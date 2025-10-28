"""
=== Conversion d’un fichier LiDAR en tableau NumPy ===

Ce code permet de :
- Convertir un fichier LiDAR en tableau NumPy structuré.
- Adapter le niveau de détail des attributs extraits selon le besoin (complet, partiel ou utile).

Informations complémentaires :
- Ce script constitue une étape essentielle pour le traitement ultérieur des données LiDAR.
- Il permet de préparer les données sous un format compatible avec les traitements NumPy.

"""

# === Importations ===

import numpy as np

from import_LIDAR import laz_to_las



# === Fonctions principales ===

def afficher_attributs_disponibles(las):
    """Affiche les attributs disponibles du fichier las afin de choisir les attributs que l'on veut garder grâce aux fonctions suivantes"""
    
    attributs = list(las.point_format.dimension_names)
    return attributs



def LIDAR_numpy_complet(las):
    """Construction du tableau Numpy avec tous les attributs"""

    # Récupération de tous les attributs disponibles
    attributs_voulus = list(las.point_format.dimension_names)

    # Construction du tableau Numpy
    dtype = [(attr, las[attr].dtype) for attr in attributs_voulus]
    tableau_point = np.zeros(len(las.points), dtype=dtype)

    # Remplissage du tableau
    for attr in attributs_voulus:
        tableau_point[attr] = las[attr]

    return tableau_point



def LIDAR_numpy_incomplet(las):
    """Construction du tableau Numpy avec uniquement les attributs : X, Y, Z, intensity, return_number, number_of_returns, classification, x, y, z"""

    # Attributs voulus 
    attributs_voulus = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns", "classification"] 

    # Construction du tableau Numpy avec 'attributs_voulus' et 'coords_converties'
    dtype = [(attr, las[attr].dtype) for attr in attributs_voulus] + [(coords_converties, np.float64) for coords_converties in ["x","y","z"]]
    tableau_point = np.zeros(len(las.points), dtype=dtype)

    # Remplissage du tableau avec les attributs demandés et les coordonnées converties
    for attr in attributs_voulus:
        tableau_point[attr] = las[attr]

    tableau_point["x"] = las.X * las.header.scale[0] + las.header.offset[0]
    tableau_point["y"] = las.Y * las.header.scale[1] + las.header.offset[1]
    tableau_point["z"] = las.Z * las.header.scale[2] + las.header.offset[2]

    return tableau_point



def LIDAR_numpy_utile(las):
    """Construction du tableau Numpy avec uniquement les attributs : classification, x, y, z"""

    # Attributs voulus 
    attributs_voulus = ["classification"] 

    # Construction du tableau Numpy avec 'attributs_voulus' et 'coords_converties'
    dtype = [(attr, las[attr].dtype) for attr in attributs_voulus] + [(coords_converties, np.float64) for coords_converties in ["x","y","z"]]
    tableau_point = np.zeros(len(las.points), dtype=dtype)

    # Remplissage du tableau avec les attributs demandés et les coordonnées converties
    for attr in attributs_voulus:
        tableau_point[attr] = las[attr]

    tableau_point["x"] = las.X * las.header.scale[0] + las.header.offset[0]
    tableau_point["y"] = las.Y * las.header.scale[1] + las.header.offset[1]
    tableau_point["z"] = las.Z * las.header.scale[2] + las.header.offset[2]

    return tableau_point



# === Lancement du script ===

if __name__ ==  "__main__" :

    # === Chargement du fichier LiDAR ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    las = laz_to_las(file_path)

    # === Affichage des attributs disponibles ===
    attributs_disponibles = afficher_attributs_disponibles(las)
    print(f"\nAttributs disponibles :")
    print(attributs_disponibles)

    # === Construction du tableau NumPy complet ===
    tableau_point = LIDAR_numpy_complet(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec tous les attributs ===")
    print(tableau_point[:5])

    # === Construction du tableau NumPy incomplet ===
    tableau_point = LIDAR_numpy_incomplet(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec uniquement certains attributs ===")
    print(tableau_point[:5])

    # === Construction du tableau NumPy utile ===
    tableau_point = LIDAR_numpy_utile(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec les attributs utiles ===")
    print(tableau_point[:5])
