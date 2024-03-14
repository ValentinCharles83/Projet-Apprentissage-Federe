import matplotlib.pyplot as plt

# Données pour les graphiques
clients = [1, 3, 5, 7]
accuracy_poisoning = [0.1, 0.1, 0.1, 0.1]
accuracy_flipping = [0.5199, 0.4652, 0.2704, 0.1109]

# Création des graphiques
plt.figure(figsize=(14, 6))

# Graphique pour Model Poisoning
plt.subplot(1, 2, 1)
plt.plot(clients, accuracy_poisoning, marker='o', linestyle='-', color='r')
plt.title('Impact of Model Poisoning Attack')
plt.xlabel('Number of Malicious Clients')
plt.ylabel('Model Accuracy')
plt.xticks(clients)
plt.ylim(0, 0.6)

# Graphique pour Label Flipping
plt.subplot(1, 2, 2)
plt.plot(clients, accuracy_flipping, marker='o', linestyle='-', color='b')
plt.title('Impact of Label Flipping Attack')
plt.xlabel('Number of Malicious Clients')
plt.ylabel('Model Accuracy')
plt.xticks(clients)
plt.ylim(0, 0.6)

# Affichage des graphiques
plt.tight_layout()
plt.savefig("attack_impact_10clients.png")
plt.show()
