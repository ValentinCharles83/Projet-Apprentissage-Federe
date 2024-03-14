import matplotlib.pyplot as plt

# Données pour les deux types d'attaque
malicious_clients_label_flipping = [1, 2, 3]
final_accuracy_label_flipping = [0.5607, 0.311, 0.0711]
malicious_clients_model_poisoning = [1, 2, 3]
final_accuracy_model_poisoning = [0.1063, 0.0999, 0.0999]

# Configuration du graphique
plt.figure(figsize=(12, 8))

# Tracé pour label flipping
plt.plot(malicious_clients_label_flipping, final_accuracy_label_flipping, marker='o', linestyle='-', color='b', label='Label Flipping')

# Tracé pour model poisoning
plt.plot(malicious_clients_model_poisoning, final_accuracy_model_poisoning, marker='s', linestyle='-', color='r', label='Model Poisoning')

# Titre, légende et étiquettes des axes
plt.title('Impact des Clients Malveillants sur la Précision du Modèle')
plt.xlabel('Nombre de Clients Malveillants')
plt.ylabel('Précision du Modèle Final')
plt.legend()

# Configuration de la grille, des ticks et des limites
plt.grid(True)
plt.xticks([1, 2, 3])
plt.ylim(0, 0.6)

# Sauvegarde du graphique
plt.savefig('attack_impact_3clients.png')

# Affichage du graphique
plt.show()
