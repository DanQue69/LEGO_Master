"""
=== Conversion d’un fichier LiDAR en DataFrame ===

Ce code permet de :
- Convertir un fichier LiDAR en DataFrame structuré.
- Adapter le niveau de détail des attributs extraits selon le besoin (complet, partiel ou utile).

Informations complémentaires :
- Ce script ne sera pas utilisé ultérieurement car nous avons choisi de stocker nos données sous le format Numpy.

"""

# === Importations ===

import pandas as pd

from import_LIDAR import laz_to_las



# === Fonctions principales ===

def afficher_attributs_disponibles(las):
    """Affiche les attributs disponibles du fichier las afin de choisir les attributs que l'on veut garder grâce aux fonctions suivantes"""

    attributs = list(las.point_format.dimension_names)
    return attributs



def LIDAR_DataFrame_complet(las):
    """Construction d'un DataFrame avec tous les attributs"""

    # Récupération de tous les attributs disponibles
    attributs_voulus = list(las.point_format.dimension_names)

    df = pd.DataFrame({attr: las[attr] for attr in attributs_voulus})
    return df



def LIDAR_DataFrame_incomplet(las):
    """Construction d'un DataFrame avec uniquement les attributs : X, Y, Z, intensity, return_number, number_of_returns, classification, x, y, z"""

    attributs_voulus = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns", "classification"]

    df = pd.DataFrame({
        **{attr: las[attr] for attr in attributs_voulus},  
        "x": las.X * las.header.scale[0] + las.header.offset[0],
        "y": las.Y * las.header.scale[1] + las.header.offset[1],
        "z": las.Z * las.header.scale[2] + las.header.offset[2]
    })

    return df



def LIDAR_DataFrame_utile(las):
    """Construction d'un DataFrame avec uniquement les attributs : classification, x, y, z"""

    attributs_voulus = ["classification"]

    df = pd.DataFrame({
        "classification": las["classification"],
        "x": las.X * las.header.scale[0] + las.header.offset[0],
        "y": las.Y * las.header.scale[1] + las.header.offset[1],
        "z": las.Z * las.header.scale[2] + las.header.offset[2]
    })

    return df



# === Lancement du script ===

if __name__ ==  "__main__" :

    # === Chargement du fichier LiDAR ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    las = laz_to_las(file_path)

    # === Affichage des attributs disponibles ===
    attributs_disponibles = afficher_attributs_disponibles(las)
    print(f"\nAttributs disponibles :")
    print(attributs_disponibles)

    # === Construction d'un DataFrame complet ===
    df_complet = LIDAR_DataFrame_complet(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec tous les attributs ===")
    print(df_complet.head())

    # === Construction d'un DataFrame incomplet ===
    df_incomplet = LIDAR_DataFrame_incomplet(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec uniquement certains attributs ===")
    print(df_incomplet.head())

    # === Construction d'un DataFrame utile ===
    df_utile = LIDAR_DataFrame_utile(las)                                       
    print("\n=== Aperçu des 5 premiers points transformés avec les attributs utiles ===")
    print(df_utile.head())

