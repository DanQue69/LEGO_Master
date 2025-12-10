"""
=== Affichage d'un fichier LiDAR (.laz) ===

Ce code permet de :
- Afficher les métadonnées du header du fichier 
- Lister les attributs disponibles pour chaque point
- Afficher un aperçu des attributs des n premiers points

Informations complémentaires :
- Ce code est surtout une aide pour quiconque veut comprendre la composition d'un fichier LIDAR.
- Il ne contribue pas directement à la finalité opérationnelle du projet, mais en constitue un support d’analyse.

"""

# === Importations ===

import laspy

from import_LIDAR import laz_to_las



# === Fonctions principales ===

def afficher_header(las):
    """Affiche le header du fichier LiDAR."""

    print("=== Header du fichier ===")
    print(las.header)

    print("\n=== Détails du header ===")
    for attr in dir(las.header):
        if not attr.startswith("_") and not callable(getattr(las.header, attr)):
            print(f"{attr} : {getattr(las.header, attr)}")



def afficher_coordonnees_systeme(las):
    """Affiche le système de coordonnées du fichier LiDAR."""

    print("\n=== Système de coordonnées ===")
    try:
        vlr_wkt = las.header.vlrs[1]
        print(vlr_wkt.string)
    except (IndexError, AttributeError):
        print("Aucun VLR WKT trouvé (système de coordonnées inconnu).")



def afficher_bornes_zone(las):
    """Affiche les bornes spatiales (min et max) du nuage de points."""

    print("\n=== Bords de la zone ===")
    print("Min :", las.header.min)
    print("Max :", las.header.max)



def afficher_infos_fichier(las):
    """Affiche les informations sur le système et le logiciel d'origine."""

    print("\n=== Infos du fichier ===")
    print("Système :", las.header.system_identifier)
    print("Logiciel :", las.header.generating_software)



def afficher_conversion(las):
    """Affiche la fonction de conversion entre coordonnées brutes et réelles."""

    print("\n=== Fonction de conversion ===")
    scale = las.header.scales[0]
    offset = las.header.offsets[0]
    print(f"([X,Y,Z] * {scale}) + {offset}")



def afficher_attributs_points(las):
    """Liste tous les attributs disponibles pour les points."""

    print("\n=== Attributs disponibles pour chaque point ===")
    for attr in las.point_format.dimension_names:
        print("-", attr)



def afficher_exemple_points(las, n=5):
    """Affiche les informations détaillées pour les n premiers points."""

    print(f"\n=== Exemple des {n} premiers points ===")
    for i in range(min(n, len(las.points))):
        print(f"\nPoint {i+1} :")
        # Coordonnées brutes et converties
        print(f"  X brut : {las.X[i]}  -> converti : {las.x[i]}")
        print(f"  Y brut : {las.Y[i]}  -> converti : {las.y[i]}")
        print(f"  Z brut : {las.Z[i]}  -> converti : {las.z[i]}")

        # Autres attributs
        for attr in las.point_format.dimension_names:
            if attr not in ["X", "Y", "Z"]: # X,Y,Z déjà affichés
                print(f"  {attr} : {getattr(las, attr)[i]}")



# === Lancement du script ===

if __name__ == "__main__":

    # === Chemin vers le fichier .laz ===
    file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"

    # === Lecture du fichier LiDAR ===
    print("Lecture du fichier LiDAR...")
    las = laz_to_las(file_path)

    # === Affichage des informations contenues dans le header et des attributs ===
    afficher_header(las)
    afficher_coordonnees_systeme(las)
    afficher_bornes_zone(las)
    afficher_infos_fichier(las)
    afficher_conversion(las)

    print("\nNombre total de points :", len(las.points))

    afficher_attributs_points(las)

    # === Demande à l'utilisateur combien de points afficher ===
    try:
        n = int(input("\nCombien de points à afficher ? "))
    except ValueError:
        n = 5  # Valeur par défaut
        print("Valeur incorrecte, affichage des 5 premiers points par défaut.")

    afficher_exemple_points(las, n)









