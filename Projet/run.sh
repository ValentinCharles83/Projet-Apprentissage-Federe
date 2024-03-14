echo "Starting server"
python server.py --round 10 &
sleep 3  # Sleep for 3s to give the server enough time to start

malicious_clients=(1 3 5)  # IDs des clients malveillants
total_clients=10

for (( i=0; i<$total_clients; i++ )); do
    if [[ " ${malicious_clients[@]} " =~ " ${i} " ]]; then
        echo "Starting malicious client $i"
        python client_mal.py --node_id $i --n $total_clients --dataset CIFAR10 --data_split non_iid_class --local_epochs 1 --attack_type model_poisoning &
    else
        echo "Starting client $i"
        python client.py --node_id $i --n $total_clients --dataset CIFAR10 --local_epochs 1 &
    fi
done

# This will allow you to use CTRL+C to stop all background processes
trap "kill 0" SIGINT SIGTERM EXIT

wait
