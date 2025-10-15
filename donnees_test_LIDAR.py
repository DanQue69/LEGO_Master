"""=== Bibliothèques ==="""
import numpy as np
import pandas as pd
from import_LIDAR import laz_to_las


"""=== Code ==="""

def LIDAR_test(file_path, nb_points, taille_zone):

    # Lecture du fichier LiDAR
    las = laz_to_las(file_path)

    # Conversion des coordonnées en mètres
    x = las.X * las.header.scales[0] + las.header.offsets[0]
    y = las.Y * las.header.scales[1] + las.header.offsets[1]
    z = las.Z * las.header.scales[2] + las.header.offsets[2]
    classification = las.classification

    # Sélection d’une zone carrée aléatoire 
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)

    x0 = np.random.uniform(xmin, xmax - taille_zone)
    y0 = np.random.uniform(ymin, ymax - taille_zone)

    # Points dans la zone
    masque_zone = (x >= x0) & (x <= x0 + taille_zone) & (y >= y0) & (y <= y0 + taille_zone)
    indices_zone = np.where(masque_zone)[0]

    # Si trop de points, on échantillonne
    if len(indices_zone) > nb_points:
        indices_zone = np.random.choice(indices_zone, size=nb_points, replace=False)

    # --- Données finales ---
    x_sel = x[indices_zone]
    y_sel = y[indices_zone]
    z_sel = z[indices_zone]
    classification_sel = classification[indices_zone]

    # --- Tableau Numpy ---
    LIDAR_numpy_test = np.zeros(len(indices_zone), dtype=[
        ('x', np.float64),
        ('y', np.float64),
        ('z', np.float64),
        ('classification', np.uint8)
    ])
    LIDAR_numpy_test['x'] = x_sel
    LIDAR_numpy_test['y'] = y_sel
    LIDAR_numpy_test['z'] = z_sel
    LIDAR_numpy_test['classification'] = classification_sel

    # --- DataFrame équivalent ---
    LIDAR_DataFrame_test = pd.DataFrame({
        'x': x_sel,
        'y': y_sel,
        'z': z_sel,
        'classification': classification_sel
    })[['x', 'y', 'z', 'classification']]

    return LIDAR_numpy_test, LIDAR_DataFrame_test



if __name__ == "__main__":

    # test

    LIDAR_numpy_test, LIDAR_DataFrame_test = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", 500, 20)
    print(LIDAR_numpy_test)
    print(LIDAR_DataFrame_test)