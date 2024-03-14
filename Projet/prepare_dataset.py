import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split, Subset
from torchvision.datasets import CIFAR10


def load_datasets(num_clients: int, dataset: str, data_split: str):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    if dataset == "CIFAR10":
        trainset = CIFAR10("./dataset", train=True, download=True, transform=transform)
        testset = CIFAR10("./dataset", train=False, download=True, transform=transform)
    else:
        raise NotImplementedError("The dataset is not implemented")

    if data_split == "iid":
        total_size = len(trainset)
        part_size = total_size // num_clients
        sizes = [part_size for _ in range(num_clients-1)]
        sizes.append(total_size - sum(sizes))
        datasets = random_split(trainset, sizes, generator=torch.Generator().manual_seed(42))
    elif data_split == "non_iid_class":
        # Création d'une distribution non IID basée sur les classes
        num_classes = 10  # Pour CIFAR-10
        class_indices = [[] for _ in range(num_classes)]

        for idx, (_, label) in enumerate(trainset):
            class_indices[label].append(idx)

        datasets = []
        # Assurer une distribution inégale des classes par client
        classes_per_client = num_classes // num_clients
        extra_classes = num_classes % num_clients
        start_class = 0

        for client_id in range(num_clients):
            client_indices = []
            end_class = start_class + classes_per_client + (1 if client_id < extra_classes else 0)
            for class_idx in range(start_class, end_class):
                client_indices += class_indices[class_idx]
            start_class = end_class
            client_subset = Subset(trainset, client_indices)
            datasets.append(client_subset)

    trainloaders = []
    valloaders = []
    for ds in datasets:
        len_val = len(ds) // 10  # 10% validation set
        len_train = len(ds) - len_val
        ds_train, ds_val = random_split(ds, [len_train, len_val], generator=torch.Generator().manual_seed(42))
        trainloaders.append(DataLoader(ds_train, batch_size=32, shuffle=True))
        valloaders.append(DataLoader(ds_val, batch_size=32))
    testloader = DataLoader(testset, batch_size=32)

    return trainloaders, valloaders, testloader



def get_data_loader(num_clients: int, cid: int, dataset = "CIFAR10", data_split = "iid"):
    trainloaders, valloaders, testloader = load_datasets(num_clients, dataset, data_split)
    return trainloaders[cid], valloaders[cid], testloader