# Collecte de données web sur metmuseum.org par API

## Contexte

J'ai décidé d'utiliser l'API du Metropolitanian
Museum of Art pour en savoir plus sur leurs
peintures faites en Europe. Je n'ai pas directement
utilisé une récolte en utilisant le département
peintures européennes, car celui-ci contenait des
peintures sans géolocalisation, et certaines
peintures faites en Europe étaient dans d'autres
départements.

## Organisation

Pour optimiser le temps de collecte, j'ai utilisé
la bibliothèque [httpx](https://github.com/projectdiscovery/httpx).
Celle-ci me permet de faire des requêtes dans des
fonctions asynchrones. A la racine se trouvent
plusieurs fichiers, **metmuseum.py** est un module
fournissant un ensemble de fonctions asynchrones
pour récupérer différentes info depuis l'API sans
devoir manipuler les url. **nettoyage.py** est le
fichier qui contient les fonctions pour nettoyer
les données, et **nationalities.json** est un
fichier qui contient des données pour corriger
des données. Enfin, **collecte.py** est le fichier
qui s'occupe de collecter les données et de les
exporter, il est le seul à éxecuter.

Dans le dossier shiny se trouvent tous les fichiers
nécessaires pour le tableau de bord shiny et des
données dans le sous-dossier data.

## Mise en place

Installer les dépendances :
```bash
pip install -r requirements.txt -r shiny/requirements.txt
```

Ajouter shiny dans le PATH :
```bash
export PATH=$PATH:"~/.local/bin"
```

## Execution

Lancer le script de collecte puis le tableau de 
bord shiny :
```bash
python3 collecte.py && cd shiny; shiny run --reload
```

Lancer seulement le tableau de bord :

```bash
ch shiny
shiny run --reload
```
