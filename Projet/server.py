import flwr as fl
from typing import List, Tuple
from flwr.common import Metrics
import argparse
import torch.nn as nn
import torch.nn.functional as F
import torch
from collections import OrderedDict
from tqdm import tqdm
import prepare_dataset
from flwr.server.strategy import FedMedian
from flwr.server.strategy import FedTrimmedAvg

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
parser = argparse.ArgumentParser(description="Flower")
parser.add_argument(
    "--round",
    type=int,
    default=10,
    help="Partition of the dataset divided into 3 iid partitions created artificially.",
)
rounds = parser.parse_args().round

class Net(nn.Module):
    """Model"""

    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


def test(net, testloader):
    """Validate the model on the validation set."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, loss = 0, 0.0
    with torch.no_grad():
        for images, labels in tqdm(testloader, "Testing"):
            outputs = net(images.to(DEVICE))
            labels = labels.to(DEVICE)
            loss += criterion(outputs, labels).item()
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
    accuracy = correct / len(testloader.dataset)
    return loss, accuracy


# The `evaluate` function will be by Flower called after every round
def evaluate_function():
    def evaluate(server_round, parameters, config):
        net = Net().to(DEVICE)
        params_dict = zip(net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        net.load_state_dict(state_dict, strict=True)
        _ ,_ , testloader = prepare_dataset.load_datasets(2, "CIFAR10", "iid")
        loss, accuracy = test(net, testloader)
        print(f"Round {server_round}: Server-side evaluation loss {loss} / accuracy {accuracy}")
        return loss, {"accuracy": accuracy}
    return evaluate


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]):
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    round = metrics[0][1]["round"]
    examples = [num_examples for num_examples, _ in metrics]
    accuracy = sum(accuracies) / sum(examples)
    print(f"Round {round} Global model test accuracy: {accuracy}")
    # Aggregate and return custom metric (weighted average)
    try:
        with open('log.txt', 'a') as f:
            if round == 1:
                f.write("\n-------------------------------------\n")
            f.write(str(accuracy)+" ")
    except FileNotFoundError:
        with open('log.txt', 'w') as f:
            if round == 1:
                f.write("\n-------------------------------------\n")
            f.write(str(accuracy)+" ")

    return {"accuracy": {accuracy}}


def fit_config(server_round:int):
    config = {
        "server_round": server_round,
    }
    return config


strategy = FedTrimmedAvg(
    beta=0.4,
    on_fit_config_fn=fit_config,
    on_evaluate_config_fn=fit_config,
    evaluate_fn=evaluate_function(),
)

fl.server.start_server(
    server_address="0.0.0.0:8081",
    config=fl.server.ServerConfig(num_rounds=rounds),
    strategy=strategy
)