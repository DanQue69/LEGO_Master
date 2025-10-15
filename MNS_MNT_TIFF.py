"""=== Bibliothèque ==="""

import numpy as np
import rasterio
from rasterio.transform import from_origin

from donnees_test_LIDAR import LIDAR_test
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_DataFrame import LIDAR_DataFrame_utile
from LIDAR_MNS_MNT import numpy_MNS, DataFrame_MNS



"""=== Code ==="""

def MNS_TIFF_numpy(grid, bounds, grid_size=1.0, nan_color=(255, 0, 0), save_path="MNS.tif"):


    x_min, y_min, x_max, y_max = bounds

    # Normalisation 0–255
    z_min, z_max = np.nanmin(grid), np.nanmax(grid)
    norm = (grid - z_min) / (z_max - z_min) * 255
    norm = np.clip(norm, 0, 255)
    gray = np.nan_to_num(norm, nan=0).astype(np.uint8)

    # Conversion en RGB + couleur NaN
    rgb = np.stack([gray]*3, axis=-1)
    mask_nan = np.isnan(grid)
    rgb[mask_nan] = nan_color

    # inversion verticale
    rgb = np.flipud(rgb)

    # Création du GeoTIFF avec coordonnées réelles
    height, width = grid.shape
    transform = from_origin(x_min, y_max, grid_size, grid_size)  # coordonnée réelle

    with rasterio.open(
        save_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=3,
        dtype='uint8',
        crs='EPSG:2154',
        transform=transform
    ) as dst:
        for i in range(3):
            dst.write(rgb[:, :, i], i + 1)

    return rgb






if __name__ == "__main__":

    # test
    
    # test_LIDAR_numpy, test_LIDAR_DataFrame = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", 2000, 50)
    # MNS_numpy, bornes = numpy_MNS(test_LIDAR_numpy, grid_size=1.0)
    # TIFF = MNS_TIFF_numpy(MNS_numpy, bornes, grid_size=1.0, nan_color=(255, 0, 0), save_path="MNS.tif")

    las = laz_to_las("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz")
    LIDAR_numpy = LIDAR_numpy_utile(las)
    MNS_numpy, bornes = numpy_MNS(LIDAR_numpy, grid_size=1.0)
    TIFF = MNS_TIFF_numpy(MNS_numpy, bornes, grid_size=1.0, nan_color=(255, 0, 0), save_path="MNS.tif")


