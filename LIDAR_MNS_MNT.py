"""=== Bibliothèque ==="""

import numpy as np
from donnees_test_LIDAR import LIDAR_test
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_DataFrame import LIDAR_DataFrame_utile


"""=== Code ==="""

""" Fonction de création de grille """

def creer_grille(x, y, z, grid_size=1.0, agg_func=np.nanmax):

    # Étendue de la zone
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Dimension de la grille
    nx = int(np.ceil((x_max - x_min) / grid_size))
    ny = int(np.ceil((y_max - y_min) / grid_size))

    # Conversion en indices
    xi = ((x - x_min) / grid_size).astype(int)
    yi = ((y - y_min) / grid_size).astype(int)

    # Filtrage des points valides
    valid = (xi >= 0) & (xi < nx) & (yi >= 0) & (yi < ny)
    xi, yi, z = xi[valid], yi[valid], z[valid]

    # Index linéaire
    flat_index = yi * nx + xi

    # Grille initialisée à -inf (pour éviter le warning)
    grid_flat = np.full(ny * nx, -np.inf)

    # Agrégation (max par cellule) => c'est ça qui rend le code plus rapide car codé en C
    np.maximum.at(grid_flat, flat_index, z)

    # Remplacer -inf par NaN pour les cases vides
    grid_flat[grid_flat == -np.inf] = np.nan

    # Reshape en 2D
    grid = grid_flat.reshape((ny, nx))

    return grid, (x_min, y_min, x_max, y_max)


""" Fonctions NumPy """

def numpy_MNS(numpy, grid_size=1.0):
    """Crée un MNS à partir d’un tableau NumPy."""
    grille, bornes = creer_grille(numpy["x"], numpy["y"], numpy["z"], grid_size, agg_func=np.nanmax)
    return grille, bornes



""" Fonctions DataFrame """

def DataFrame_MNS(DataFrame, grid_size=1.0):
    """Crée un MNS à partir d’un DataFrame LiDAR."""
    grille, bornes = creer_grille(DataFrame["x"], DataFrame["y"], DataFrame["z"], grid_size, agg_func=np.nanmax)
    return grille, bornes



if __name__ == "__main__":
    
    # test
    # test_LIDAR_numpy, test_LIDAR_DataFrame = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", 1000, 10)
    # MNS_numpy, bornes = numpy_MNS(test_LIDAR_numpy, grid_size=1.0)
    # print("Bornes :", bornes)
    # print(MNS_numpy)
    
    
    
    
    las = laz_to_las("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz")

    LIDAR_numpy = LIDAR_numpy_utile(las)
    # LIDAR_DataFrame = LIDAR_DataFrame_utile(las)

    MNS_numpy = numpy_MNS(LIDAR_numpy, grid_size=1.0)
    # MNS_DataFrame = DataFrame_MNS(LIDAR_DataFrame, grid_size=1.0)

    # print(MNS_numpy)



