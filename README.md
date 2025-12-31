# Projet LiDAR to LEGO 

Ce projet propose une chaîne de traitement complète ("pipeline") permettant de convertir des nuages de points LiDAR (format .laz) en modèles 3D constitués de briques LEGO (format .ldr).

Conçu dans le cadre d'un Projet d'Initiation à la Recherche (ING2 - ENSG), le code est optimisé pour traiter les données LiDAR HD de l'IGN (France).

---

## Architecture du projet

```text
PROJET_RACINE/
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


