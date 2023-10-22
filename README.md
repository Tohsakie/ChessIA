# Exemple d'Application Modèle d'Echec 

Ce projet est un exemple d'application de notre IA basé sur l'apprentissage des meilleurs coups possible aux échecs.

Il permet de jouer aux échecs en affrontant notre IA. Les utilisateurs peuvent jouer aux échecs en déplaçant les pièces sur un échiquier, et le système peut prédire le prochain mouvement possible à l'aide d'une API.


## Dépendances 


```bash
pip install Flask
pip install torch
pip install numpy
pip install pandas
pip install python-chess
```

Puis, télécharger l'archive [DataSet](https://www.kaggle.com/datasets/ronakbadhe/chess-evaluations/download?datasetVersionNumber=4) et placer "tactic_evals.csv" dans le dossier /api

## Utilisation
### Interface utilisateur
Pour jouer aux échecs, il suffit de lancer la page **main.html** situé dans le dossier /web

Vous pouvez entrer la notation FEN (Forsyth-Edwards Notation) dans le champ de texte pour définir une position spécifique.

Appuyez sur le bouton "Reset" pour réinitialiser la position à la configuration de départ.

### Prédiction de mouvement

- Le bouton "Predict" ainsi que le déplacement d'une pièce appelle l'API pour prédire le prochain mouvement. 

- L'API est exécutée localement à l'adresse http://localhost:8000/predict/.

- La prédiction est basée sur la position actuelle de l'échiquier.


### API
- L'API est développée en Python avec Flask. Voici comment elle fonctionne :

- L'API reçoit la notation FEN via une requête POST.

- Elle utilise le appelé commons pour prédire le prochain mouvement en fonction de la position.

- La prédiction est renvoyée au client sous forme de message JSON.

### Exécution de l'API

Pour exécuter l'API, assurez-vous d'avoir Flask installé, puis exécutez le script Python api.py.

```bash
Copy code
python3  api/app.py
```

L'API sera accessible à l'adresse http://localhost:8000/.

*Si le port 8000 est déjà pris, il est nécessaire de le changer dans chess.js ainsi que app.py*


## Auteur

Ce projet a été créé par :
* Boubou Jean-Philippe
* HACQUARD Grégorie
* MASSET Eliot