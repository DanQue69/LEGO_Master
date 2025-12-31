# Projet LiDAR to LEGO 

Ce projet propose une chaîne de traitement complète ("pipeline") permettant de convertir des nuages de points LiDAR (format .laz) en modèles 3D constitués de briques LEGO (format .ldr).

Conçu dans le cadre d'un Projet d'Initiation à la Recherche (ING2 - ENSG), le code est optimisé pour traiter les données LiDAR HD de l'IGN (France).



PROJET_RACINE/
│
├── data/              # Dossier destiné aux fichiers .laz (ex: sample.laz)
│                      # ⚠️ Les fichiers >100Mo ne sont pas inclus sur GitHub.
│
├── docs/              # Documentation, rapports et illustrations du projet.
│
├── outputs/           # Dossier généré automatiquement contenant les résultats :
│   ├── Avant_Traitement/   # Modèles bruts (voxelisation simple).
│   ├── Apres_Traitement/   # Modèles finaux (nettoyés, colorés et consolidés).
│   └── LIDAR_couches/      # (Optionnel) Exports GeoTIFF couche par couche.
│
├── src/               # Code source Python (Modules) :
│   ├── import_LIDAR.py                 # Lecture LAS/LAZ
│   ├── affichage_LIDAR.py              # Visualisation des métadonnées
│   ├── LIDAR_numpy.py                  # Conversion LAS -> Numpy
│   ├── LIDAR_couches.py                # Voxelisation & Export GeoTIFF
│   ├── LIDAR_traitement.py             # Algorithmes de graphes & structure
│   ├── LIDAR_LDRAW.py                  # Génération fichiers .ldr
│   └── donnees_echantillonnees_LIDAR.py # Outils de test (échantillonnage)
│
├── main.py            # 🚀 Point d'entrée principal (Configuration & Exécution)
├── requirements.txt   # Liste des dépendances Python
├── .gitignore         # Configuration Git (exclusion venv, gros fichiers)
└── README.md          # Ce fichier


