# Projet : Attaque et Défense dans l'apprentissage fédéré

## Rapport de Valentin Charles (Label_flipping) et Adem Ben Jabria (Model_poisoning)

Date de rendu : 14/03/2024




Question : Quel est le retour du client malveillant au serveur ? Comparez avec le cas où
les deux clients sont honnêtes. Quelle est votre observation sur le modèle obtenu ?

Réponse : L'exécution avec deux clients non malveillants montre une amélioration significative et constante du modèle global en termes de précision et de perte. Dès le premier round, la perte diminue de manière significative de 721.166 à 489.888, et la précision augmente à 0.4201, poursuivant cette tendance positive jusqu'à atteindre une perte de 346.904 et une précision de 0.6132 au round 10. Cela contraste avec le scénario incluant un client malveillant, où les améliorations étaient moins prononcées et les échecs d'évaluation étaient fréquents.

Cette comparaison révèle l'impact négatif d'un client malveillant sur le processus d'apprentissage fédéré. Même si le système peut progresser, la présence d'un client malveillant peut ralentir l'amélioration globale du modèle et potentiellement introduire des échecs d'évaluation, comme observé dans les logs. En l'absence de comportement malveillant, le modèle s'améliore de manière plus efficace et cohérente, soulignant l'importance de la confiance et de la vérification dans les environnements d'apprentissage fédéré.


## Attaque active : 
### Attaque active :  Inversion d'étiquettes (Binôme I) 
1. Dans le fichier client_mal.py qui présente les clients malveillants,
implémentez l'attaque "inversion d'étiquettes" dans la fonction train. Par exemple, pour CIFAR10, tous les "labels" seront décalés d'un.

### Attaque active :  Altération du modèle (Binôme II)
1. Dans le fichier client_mal.py qui présente les clients malveillants,
implémentez l'attaque "altération du modèle" dans la fonction train. Au lieu d'appliquer la descente de gradient,
le client appliquera une montée de gradient.

**Réponses** : 
Méthode train de client_mal.py contenant les deux 
implémentations : 
```
def train(net, trainloader, epochs, attack_type):
    """Train the model on the training set."""
    # Définir le critère de perte et l'optimiseur hors des conditions d'attaque
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

    for epoch in range(epochs):
        for images, labels in tqdm(trainloader, "Training"):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = net(images)

            if attack_type == "label_flipping":
                # Shift labels by one for label flipping attack
                labels = (labels + 1) % 10
            
            loss = criterion(outputs, labels)
            loss.backward()

            if attack_type == "model_poisoning":
                # Invert gradients for model poisoning
                with torch.no_grad():
                    for param in net.parameters():
                        param.grad = -param.grad

            optimizer.step()
```
**Chacun répond les questions suivantes sur leur attaque implémentée** :
1. Testez votre code sur un scénario avec quatre clients. Augmentez le nombre de clients malveillants de 1 à 3.
Quelle est votre observation sur le modèle obtenu et pourquoi ? Affichez un graphique où l'axe des abscisses représente le nombre de clients malveillants et l'axe des ordonnées représente la précision du modèle final.

**Réponses** : graphique=(attack_impact_3clients.png)

*label_flipping* : 

L'impact des clients malveillants utilisant l'attaque de "label flipping" sur la précision du modèle est manifeste : avec un seul client malveillant, la précision reste à 0.5607, illustrant une certaine résilience du modèle. Toutefois, en augmentant le nombre de clients malveillants à 2, la précision chute drastiquement à 0.311, et avec 3 clients malveillants, elle plonge à 0.0711. Cette baisse significative de précision avec l'augmentation des attaquants montre clairement que le "label flipping" perturbe l'apprentissage, dégradant la qualité du modèle à mesure que le nombre de contributeurs malveillants croît. Cela démontre l'importance cruciale de stratégies de défense efficaces dans l'apprentissage fédéré pour maintenir l'intégrité et la performance du modèle global face à de telles attaques.

*model_poisoning* : 

Le graphique montre l'impact des attaques de "model poisoning" sur la précision du modèle dans un scénario d'apprentissage fédéré avec quatre clients, où le nombre de clients malveillants augmente de 1 à 3. On observe que même avec un seul client malveillant, la précision du modèle chute considérablement à 0.1063, et elle reste pratiquement inchangée à 0.0999 avec deux et trois clients malveillants. Cela indique que l'attaque de "model poisoning" a un effet dévastateur dès l'introduction d'un seul client malveillant, rendant le modèle presque inutilisable, avec peu ou pas de différence dans l'impact avec l'augmentation du nombre de clients malveillants.

Cette observation suggère que les attaques de "model poisoning" sont extrêmement efficaces pour compromettre l'intégrité du modèle global dans l'apprentissage fédéré, nécessitant des mesures robustes pour détecter et atténuer ces types d'attaques afin de protéger la qualité du modèle.

2. Retestez le scénario précédent, mais cette fois avec l'option "--data_split non_iid_class". Cette attaque est-elle plus efficace
dans cette situation et pourquoi ? Utilisez des graphiques pour montrer vos résultats.

**Réponse** :  graphique=(non_iid_attacks_comparison.png)

En comparant les attaques "label flipping" et "model poisoning" dans les contextes IID et non-IID, on observe des différences notables d'efficacité. Pour le "model poisoning", la précision reste basse à 0.1 dans les deux contextes, indiquant une forte efficacité de l'attaque indépendamment de la distribution des données. Cela suggère que le "model poisoning" est une attaque profondément perturbatrice qui paralyse le modèle, que les données soient distribuées de manière IID ou non-IID.

Pour le "label flipping", dans le contexte IID, la précision diminue avec l'augmentation des attaquants, passant de 0.5607 avec un attaquant à 0.0711 avec trois, montrant une sensibilité notable du modèle à cette attaque. En non-IID, la précision finale avec un attaquant est de 0.3249, diminuant à 0.1882 avec trois attaquants, indiquant également une diminution mais à un rythme moins dramatique que dans le contexte IID.

Ces observations suggèrent que bien que les deux types d'attaques soient efficaces dans les deux contextes, le "model poisoning" a un impact dévastateur immédiat sur la précision du modèle, indépendamment de la distribution des données. Le "label flipping", bien que significativement impactant en contexte IID, voit son efficacité légèrement atténuée dans un cadre non-IID, probablement dû à la diversité et à la spécificité des sous-ensembles de données traités par chaque client.

3. Testez des scénarios plus réalistes avec 10 clients (sur NEF). Vous pouvez utiliser le script run.sh pour lancer les clients et le serveur.
Attention, vous devez modifier le script pour ajouter les clients malveillants. Étudiez les cas où il y a 1, 3, 5, 7 clients malveillants.
Utilisez des graphiques pour montrer vos résultats.

**Réponse** : Model Poisoning avec 10 clients : graphique =(attack_impact_10clients.png)

1 client malveillant : La précision reste constante à 0.1.
3 clients malveillants : La précision diminue légèrement à 0.0907.
5 clients malveillants : La précision baisse à 0.0868.
7 clients malveillants : La précision est légèrement supérieure à 0.1005.
Label Flipping avec 10 clients :
1 client malveillant : La précision augmente progressivement de 0.1 à 0.5199.
3 clients malveillants : La précision commence à 0.1 et atteint 0.4652.
5 clients malveillants : Avec une précision démarrant à 0.1004 et finissant à 0.2704.
7 clients malveillants : La précision varie de 0.104 à 0.1109.

*Model Poisoning* :

Le model poisoning montre un impact majeur dès la présence d'un seul client malveillant, avec la précision du modèle restant constamment à 0.1 quel que soit le nombre de clients malveillants. Cela indique que l'attaque de model poisoning est extrêmement efficace pour dégrader la performance du modèle global, même avec une faible proportion de clients malveillants. Il suffit d'un seul client malveillant pour rendre le modèle pratiquement inutile, soulignant la vulnérabilité du système d'apprentissage fédéré à ce type d'attaque.

*Label Flipping* :

Contrairement au model poisoning, l'efficacité de l'attaque de label flipping semble augmenter avec le nombre de clients malveillants. Bien que l'impact soit moins immédiat que celui du model poisoning, la présence accrue de clients malveillants utilisant l'attaque de label flipping entraîne une dégradation progressive de la précision du modèle. Cela suggère que le label flipping nécessite une masse critique de clients malveillants pour avoir un impact significatif, mais une fois ce seuil atteint, l'efficacité de l'attaque devient notable.

## Défense 
Appliquer la défense "Médiane par coordonnées" et "Moyenne tronquée" sur le serveur,
en utilisant la stratégie fournie par flwr: class [`FedMedian`](https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/fedmedian.py)
and class [`FedTrimmedAvg`](https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/fedtrimmedavg.py). 

Répondez aux questions suivantes pour l'attaque d'inversion d'étiquettes (Binôme I) et pour l'attaque d'altération du modèle (Binôme II) :
N'hésitez pas à utiliser des graphiques pour montrer les résultats !

1. Quelle défense est plus efficace contre l'attaque ?
2. À partir de combien de clients malveillants la défense échoue-t-elle totalement ?
3. Comparez les cas de "--data_split iid" et "--data_split non_iid_class". La défense est-elle plus efficace
    dans quelle situation et pourquoi ?

Réponse des 3 Questions : graphique =(defenses_impact.png)

*Model Poisoning* :

*Efficacité des défenses* : FedTrimmedAvg se révèle être plus efficace que FedMedian contre l'attaque de model poisoning, principalement en raison de sa capacité à exclure les extrêmes, ce qui est crucial pour atténuer les effets de cette attaque car dès qu'un client malveillant sous model poisonning peut affecter les résultats, ils
descendent instantanément à la valeur la plus basse.

D'où le fait que FedTrimmedAvg avec sa capacité d'ignorer les extrémités peut selon son réglage quasiment tout le 
temps protéger l'apprentissage.
Mon beta étant réglé à 0.2 pour les tests que j'ai fait, les attaques à 1 client ou 2 clients malveillant ne
peuvent succéder. 

*Nombre de clients malveillants pour l'échec de la défense* : Pour FedMedian, la défense s'avère inefficace dès l'introduction d'un seul client malveillant, la précision tombant à 0.1 dans tous les cas testés.
FedTrimmedAvg commence à montrer des signes d'échec avec l'introduction de trois clients malveillants, où la précision tombe également à des niveaux similaires.

*Impact du non-IID* : Les performances des deux défenses se détériorent dans un environnement non-IID, ce qui est visible par la baisse de précision et l'incapacité à maintenir l'efficacité contre les attaques. Cela montre que les différences dans la distribution des données parmi les clients augmentent la vulnérabilité des modèles à ce type d'attaque.


*Label Flipping* :

*Efficacité des défenses* : L'efficacité de FedMedian et FedTrimmedAvg contre les attaques de label flipping peut être considérée comme similaire lorsque le paramètre beta de FedTrimmedAvg est inférieur au nombre de clients malveillants. Cependant, lorsque beta est supérieur au nombre de clients malveillants, FedTrimmedAvg montre une capacité supérieure à réussir ses défenses. 
j'ai notamment testé avec un beta de 0.4 pour 3 clients et fedTrimmedAvg a réussi sa défense avec une précision
maximale la ou la précision de FedMedian est réduite de moitié

*Nombre de clients malveillants pour l'échec de la défense* : Les deux défenses présentent une dégradation progressive de la précision face à des attaques de label flipping, indiquant une absence d'échec complet mais une performance diminuant avec l'augmentation du nombre de clients malveillants. Cependant, FedTrimmedAvg peut maintenir une meilleure performance si le nombre de clients malveillants reste inférieur au seuil défini par son paramètre beta, offrant ainsi une protection plus robuste si bien paramétrée.

*Impact du non-IID* : La distribution des données non-IID introduit des complications supplémentaires pour la défense contre le label flipping pour les deux stratégies. Néanmoins, FedTrimmedAvg peut montrer une amélioration dans sa capacité à gérer ces attaques sous des conditions non-IID, probablement grâce à son mécanisme de troncature qui aide à atténuer l'impact des contributions malveillantes extrêmes. Ce bénéfice est plus prononcé lorsque beta est correctement paramétré pour exclure les mises à jour malveillantes tout en conservant suffisamment de mises à jour légitimes pour un apprentissage efficace.