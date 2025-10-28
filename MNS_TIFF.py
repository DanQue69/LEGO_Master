
"""
=== Visulisation du MNS (Modèle Numérique de Surface) à partir du tableau MNS Numpy LIDAR ===

Ce code permet de :
- Exporter le MNS en GeoTIFF avec normalisation des valeurs (0–255) et couleur spécifique pour les cellules vides (NaN).
- Adapter la résolution du MNS grâce à la taille de cellule "taille_xy" (doit être la même que l'autre "taille_xy")

Informations complémentaires :
- Ce script constitue une étape intéressante pour le traitement des données LiDAR.
- Les cellules vides (NaN) peuvent être colorées pour distinguer les zones sans points, par défaut rouge.

"""

# === Importations ===

import numpy as np
import rasterio
from rasterio.transform import from_origin

from donnees_test_LIDAR import LIDAR_test
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_DataFrame import LIDAR_DataFrame_utile
from LIDAR_MNS_MNT import numpy_MNS, DataFrame_MNS



# === Fonction principale ===

def MNS_TIFF_numpy(MNS, bornes, taille_xy, nan_color=(255, 0, 0), save_path="MNS.tif"):

    x_min, y_min, x_max, y_max = bornes

    # Normalisation 0–255
    z_min, z_max = np.nanmin(MNS), np.nanmax(MNS)
    norm = (MNS - z_min) / (z_max - z_min) * 255
    norm = np.clip(norm, 0, 255)
    gray = np.nan_to_num(norm, nan=0).astype(np.uint8)

    # Conversion en RGB + couleur NaN
    rgb = np.stack([gray]*3, axis=-1)
    mask_nan = np.isnan(MNS)
    rgb[mask_nan] = nan_color

    # Inversion verticale
    rgb = np.flipud(rgb)

    # Création du GeoTIFF avec coordonnées réelles
    hauteur, largeur = MNS.shape
    transform = from_origin(x_min, y_max, taille_xy, taille_xy)  # coordonnée réelle

    with rasterio.open(
        save_path,
        'w',
        driver='GTiff',
        height=hauteur,
        width=largeur,
        count=3,
        dtype='uint8',
        crs='EPSG:2154',
        transform=transform
    ) as dst:
        for i in range(3):
            dst.write(rgb[:, :, i], i + 1)

    return rgb






if __name__ == "__main__":

    # === IMPORT DES DONNEES ===

    # === Import des données complètes de la dalle LIDAR ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    las = laz_to_las(file_path)
    LIDAR_numpy = LIDAR_numpy_utile(las)
    MNS_numpy, bornes = numpy_MNS(LIDAR_numpy, taille_xy=1.0)

    # === Import des données échantillonnées de la dalle LIDAR ===
    test_LIDAR_numpy = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", 10000000, 265)
    test_MNS_numpy, test_bornes = numpy_MNS(test_LIDAR_numpy, taille_xy=1.0)


    # === LANCEMENT DES SCRIPTS ===
    
    # === Pour les données complètes ===
    MNS_TIFF_numpy(MNS_numpy, bornes, taille_xy=1.0, nan_color=(255, 0, 0), save_path="MNS.tif")

    # === Pour les données echantilonnées ===
    MNS_TIFF_numpy(test_MNS_numpy, test_bornes, taille_xy=1.0, nan_color=(255, 0, 0), save_path="MNS.tif")