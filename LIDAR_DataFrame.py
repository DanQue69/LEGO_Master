"""=== Bibliothèque ==="""

import pandas as pd
from import_LIDAR import laz_to_las



"""=== Code ==="""

""" Attributs disponibles """

def afficher_attributs_disponibles(las):
    # Liste des attributs disponibles
    attributs = list(las.point_format.dimension_names)
    return attributs



""" DataFrame avec tous les attributs"""

def LIDAR_DataFrame_complet(las):
    df = pd.DataFrame({attr: las[attr] for attr in attributs})
    return df



""" DataFrame avec uniquement les attributs : X, Y, Z, intensity, return_number, number_of_returns, classification, x, y, z """

def LIDAR_DataFrame_incomplet(las):
    attributs_voulus = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns", "classification"]

    df = pd.DataFrame({
        **{attr: las[attr] for attr in attributs_voulus},  
        "x": las.X * las.header.scale[0] + las.header.offset[0],
        "y": las.Y * las.header.scale[1] + las.header.offset[1],
        "z": las.Z * las.header.scale[2] + las.header.offset[2]
    })

    return df



""" DataFrame avec uniquement les attributs : classification, x, y, z """

def LIDAR_DataFrame_utile(las):
    attributs_voulus = ["classification"]

    df = pd.DataFrame({
        "classification": las["classification"],
        "x": las.X * las.header.scale[0] + las.header.offset[0],
        "y": las.Y * las.header.scale[1] + las.header.offset[1],
        "z": las.Z * las.header.scale[2] + las.header.offset[2]
    })

    return df



if __name__ == "__main__":

    # Affiche un échantillon des 5 premiers points
    print("\n=== Exemple des 5 premiers points ===")
    las = laz_to_las("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz")
    attributs_disponibles = afficher_attributs_disponibles(las)
    df = LIDAR_DataFrame_utile(las)
    print("Attributs disponibles :", attributs_disponibles)
    print(df.head())

