"""=== Bibliothèque ==="""

import numpy as np
from import_LIDAR import laz_to_las



"""=== Code ==="""

""" Attributs disponibles """

def afficher_attributs_disponibles(las):
    # Liste des attributs disponibles
    attributs = list(las.point_format.dimension_names)
    return attributs



""" Tableau Numpy avec tous les attributs"""

def LIDAR_numpy_complet(las):
    # Construction du tableau Numpy
    dtype = [(attr, las[attr].dtype) for attr in attributs]
    tableau_point = np.zeros(len(las.points), dtype=dtype)

    # Remplissage du tableau
    for attr in attributs:
        tableau_point[attr] = las[attr]

    return tableau_point



""" Tableau Numpy avec uniquement les attributs : X, Y, Z, intensity, return_number, number_of_returns, classification, x, y, z """

def LIDAR_numpy_incomplet(las):
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



""" Tableau Numpy avec uniquement les attributs : classification, x, y, z """

def LIDAR_numpy_utile(las):
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



if __name__ ==  "__main__" :

    # # Affiche un échantillon des 5 premières lignes
    # print("\n=== Exemple des 5 premiers points ===")
    las = laz_to_las("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz")
    # attributs_disponibles = afficher_attributs_disponibles(las)
    tableau_point = LIDAR_numpy_utile(las)
    # print("Attributs disponibles :", attributs_disponibles)
    # print(tableau_point[:5])