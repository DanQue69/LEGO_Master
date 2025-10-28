"""
=== Création d'un MNS (Modèle Numérique de Surface) à partir d'un tableau Numpy LIDAR ===

Ce code permet de :
- Convertir un tableau Numpy LiDAR en MNS.
- Adapter la résolution du MNS grâce à "taille_xy".

Informations complémentaires :
- Ce script constitue une étape intéressante pour le traitement des données LiDAR.
- Il permet de visualiser les données sous QGIS par exemple, bien plus simple à visualiser que les données LIDAR bruts.

"""

# === Importations ===

import numpy as np

from donnees_test_LIDAR import LIDAR_test
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_DataFrame import LIDAR_DataFrame_utile



# === Fonctions principales ===

def creer_grille(x, y, z, taille_xy, agg_func):
    """
    Génère une grille 2D MNS à partir de coordonnées LiDAR.

    Chaque cellule de la grille contient la valeur maximale de z parmi les points qui y tombent.

    Paramètres
    ----------
    x : np.ndarray
        Coordonnées x des points LiDAR.
    y : np.ndarray
        Coordonnées y des points LiDAR.
    z : np.ndarray
        Altitudes z des points LiDAR.
    taille_xy : float
        Taille d’une cellule de la grille (en mètres).

    Retour
    ------
    grid : np.ndarray
        Grille 2D du MNS (ny x nx), avec NaN pour les cellules vides.
    bornes : tuple
        Bornes du nuage de points sous la forme (x_min, y_min, x_max, y_max).
    """

    # Étendue de la zone
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Dimension de la grille
    nx = int(np.ceil((x_max - x_min) / taille_xy))
    ny = int(np.ceil((y_max - y_min) / taille_xy))

    # Conversion en indices
    ix = ((x - x_min) / taille_xy).astype(int)
    iy = ((y - y_min) / taille_xy).astype(int)

    # Filtrage des points valides
    valid = (ix >= 0) & (ix < nx) & (iy >= 0) & (iy < ny)
    ix, iy, z = ix[valid], iy[valid], z[valid]

    # Index linéaire
    index_lin = iy * nx + ix

    # Grille initialisée à -inf (pour éviter le warning)
    grid_temp = np.full(ny * nx, -np.inf)

    # Agrégation (max par cellule) => c'est ça qui rend le code plus rapide car codé en C
    np.maximum.at(grid_temp, index_lin, z)

    # Remplacer -inf par NaN pour les cases vides
    grid_temp[grid_temp == -np.inf] = np.nan

    # Reshape en 2D
    grille = grid_temp.reshape((ny, nx))

    return grille, (x_min, y_min, x_max, y_max)


""" Fonctions Numpy """

def numpy_MNS(numpy, taille_xy=1.0):
    """Crée un MNS à partir d’un tableau Numpy Lidar"""

    grille, bornes = creer_grille(numpy["x"], numpy["y"], numpy["z"], taille_xy, agg_func=np.nanmax)
    return grille, bornes



""" Fonctions DataFrame """

def DataFrame_MNS(DataFrame, taille_xy=1.0):
    """Crée un MNS à partir d’un DataFrame LiDAR"""
    
    grille, bornes = creer_grille(DataFrame["x"], DataFrame["y"], DataFrame["z"], taille_xy, agg_func=np.nanmax)
    return grille, bornes



if __name__ == "__main__":
    
    # === IMPORT DES DONNEES ===

    # === Import des données complètes de la dalle LIDAR ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    las = laz_to_las(file_path)
    LIDAR_numpy = LIDAR_numpy_utile(las)

    # === Import des données échantillonnées de la dalle LIDAR ===
    test_LIDAR_numpy = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", 10000000, 265)


    # === LANCEMENT DES SCRIPTS ===
    
    # === Pour les données complètes ===
    MNS_numpy = numpy_MNS(LIDAR_numpy, taille_xy=1.0)
    print(MNS_numpy)

    # === Pour les données echantilonnées ===
    MNS_numpy, bornes = numpy_MNS(test_LIDAR_numpy, taille_xy=1.0)
    print("Bornes :", bornes)
    print(MNS_numpy)

