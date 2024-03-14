# Ré-importation des bibliothèques nécessaires après réinitialisation de l'état d'exécution du code
import matplotlib.pyplot as plt

# Données pour model_poisoning et label_flipping avec distribution non_iid_class
malicious_clients = [1, 2, 3]

# Précision du modèle final pour model_poisoning
final_accuracy_model_poisoning = [0.1046, 0.1041, 0.0979]

# Précision du modèle final pour label_flipping
final_accuracy_label_flipping = [0.3249, 0.2923, 0.1882]

# Création des graphiques
plt.figure(figsize=(14, 7))

# Graphique pour model_poisoning
plt.subplot(1, 2, 1)
plt.plot(malicious_clients, final_accuracy_model_poisoning, marker='o', linestyle='-', color='r')
plt.title('Model Poisoning (non-IID)')
plt.xlabel('Nombre de Clients Malveillants')
plt.ylabel('Précision du Modèle Final')
plt.grid(True)
plt.xticks(malicious_clients)
plt.ylim(0, 0.4)

# Graphique pour label_flipping
plt.subplot(1, 2, 2)
plt.plot(malicious_clients, final_accuracy_label_flipping, marker='o', linestyle='-', color='b')
plt.title('Label Flipping (non-IID)')
plt.xlabel('Nombre de Clients Malveillants')
plt.ylabel('Précision du Modèle Final')
plt.grid(True)
plt.xticks(malicious_clients)
plt.ylim(0, 0.4)

# Affichage des graphiques
plt.tight_layout()
plt.savefig('non_iid_attacks_comparison.png')
plt.show()
