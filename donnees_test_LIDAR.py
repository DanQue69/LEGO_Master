"""
=== Création d'un échantillon d'un fichier LiDAR ===

Ce code permet de :
- Créer un tableau NumPy d'un échantillon d'un fichier LIDAR
- Régler les paramètres d'échantillonage via un nombre de points et d'une zone prédéfinis 

Informations complémentaires :
- Ce code est surtout destiner à échantilloner un fichier LIDAR trop important ainsi que pour tester les données sur des zones restreintes.
- Il ne contribue pas directement à la finalité opérationnelle du projet, mais en constitue un support de test.

"""

# === Importations ===

import numpy as np
import pandas as pd

from import_LIDAR import laz_to_las



# === Fonction principale ===

def LIDAR_test(file_path, nb_points, taille_zone):
    """
    Génère un échantillon sous forme de tableau NumPy à partir d’un fichier LiDAR.
    
    Paramètres
    ----------
    file_path : str
        Chemin d’accès au fichier LiDAR voulant être échantillonné.
    nb_points : int
        Nombre maximum de points souhaités dans l’échantillon.
    taille_zone : float
        Taille (en mètres) du côté de la zone carrée sélectionnée aléatoirement dans l’emprise du fichier.

    Retour
    ------
    LIDAR_numpy_test : np.ndarray
        Tableau NumPy structuré contenant les champs :
        - 'x' : coordonnées X (float64)
        - 'y' : coordonnées Y (float64)
        - 'z' : altitude Z (float64)
        - 'classification' : code de classification LiDAR (uint8)

    """

    # Lecture du fichier LiDAR
    las = laz_to_las(file_path)

    # Extraction des attributs du fichier LIDAR
    x = las.x
    y = las.y
    z = las.z
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

    # Données finales
    x_final = x[indices_zone]
    y_final = y[indices_zone]
    z_final = z[indices_zone]
    classification_final = classification[indices_zone]

    # Construction du tableau Numpy 
    LIDAR_numpy_test = np.zeros(len(indices_zone), dtype=[
        ('x', np.float64),
        ('y', np.float64),
        ('z', np.float64),
        ('classification', np.uint8)
    ])
    LIDAR_numpy_test['x'] = x_final
    LIDAR_numpy_test['y'] = y_final
    LIDAR_numpy_test['z'] = z_final
    LIDAR_numpy_test['classification'] = classification_final

    return LIDAR_numpy_test



# === Lancement du script ===

if __name__ == "__main__":

    # === Paramètres de test ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    nb_points_test = 10          # Nombre de points souhaités
    taille_zone_test = 10        # Taille (en mètres) du carré d’échantillonnage

    # === Génération de l’échantillon ===
    LIDAR_numpy_test = LIDAR_test(file_path, nb_points_test, taille_zone_test)

    # === Affichage du résultat ===
    print(f"Nombre de points retenus : {len(LIDAR_numpy_test)}")
    print(f"Taille de la zone : {taille_zone_test}x{taille_zone_test} m")
    print(f"\n{LIDAR_numpy_test}")
