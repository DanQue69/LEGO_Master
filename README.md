# Projet LiDAR_2_LEGO 

Ce projet propose une chaîne de traitement complète ("pipeline") permettant de convertir des nuages de points LiDAR (format .laz) en modèles 3D constitués de briques LEGO (format .ldr).

Conçu dans le cadre d'un Projet d'Initiation à la Recherche (ING2 - ENSG), le code est optimisé pour traiter les données LiDAR HD de l'IGN (France).

---

## Architecture du projet

```text
LiDAR_2_LEGO/
│
├── data/                      # Dossier destiné aux fichiers .laz d'entrée
│                              # Placez votre fichier .laz ici
│                              
├── docs/                      # Documentation technique, rapports et livrables
│ 
├── outputs/                   # Dossier généré automatiquement contenant les résultats (modèles bruts, traités, finales, etc...) 
│
├── src/                       # Code source Python (Modules internes) :
│   ├── affichage_LIDAR.py               # Visualisation des métadonnées du fichier LiDAR
│   ├── import_LIDAR.py                  # Lecture .laz/.las
│   ├── LIDAR_numpy.py                   # Conversion LAS -> Numpy
│   ├── donnees_echantillonnees_LIDAR.py # Echantillonage des données LiDAR
│   ├── LIDAR_couches.py                 # Voxelisation 
│   ├── LIDAR_traitement.py              # Traitements structurels des données
│   └──  LIDAR_LDRAW.py                  # Génération fichiers .ldr
│
├── main.py                    # Point d'entrée principal (Configuration & Exécution)
├── requirements.txt           # Liste des dépendances Python à installer sur votre machine
├── .gitignore                 
└── README.md                  
```

<br>

---

<br>

## Installation et Déploiement

### Prérequis

- Git : Pour cloner le projet.
- Python 3.9 ou supérieur.

<br>

### Récupération du projet

Ouvrez un terminal et clonez le dépôt sur votre machine :
```bash
git clone <URL_DU_DEPOT_GIT>
cd <NOM_DU_DOSSIER_CLONE>
```

<br>

### Installation des dépendances

Le projet utilise des librairies scientifiques et géospatiales (laspy, lazrs, numpy, networkx, rasterio). Installez-les via pip (présent depuis Python 3.4):
```bash
pip install -r requirements
```

<br>

### Gestion des données LiDAR

Un fichier `exemple.laz` est présent dans le dossier `data/`, vous pouvez lancer directement le pipeline via `main.py`.

Si vous voulez utilisez vos propres données `.laz` :
1. Téléchargez une dalle LiDAR HD via le site [Géoservices - IGN](https://cartes.gouv.fr/telechargement/IGNF_NUAGES-DE-POINTS-LIDAR-HD).
2. Placez le fichier téléchargé ou tout autre fichier `.laz` dans le dossier `data/`.
3. Ouvrez le fichier `main.py` et modifiez la variable `NOM_FICHIER` :
```python
NOM_FICHIER = "votre_fichier.laz"
```














---


---

## Crédits et Licence

- Auteurs : Romain DE BLOTEAU VALCHUK et Dan Quê NGUYEN - Géodata Paris (ex-ENSG École Nationale des Sciences Géographiques) 
- Commanditaires : Corentin LE BIHAN GAUTIER et Théo SZANTO - Laboratoire LASTIG
- Données : LiDAR HD (IGN) via la plateforme Géoservices, Licence Ouverte MIT.












