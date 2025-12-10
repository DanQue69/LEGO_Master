from donnees_test_LIDAR import LIDAR_test, LIDAR_test_rectangle
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_couches import LIDAR_couches, LIDAR_couches_LEGO, LIDAR_couches_LEGO_LDRAW
from LIDAR_LDRAW import voxel_LDRAW_classif, voxel_LDRAW
from LIDAR_traitement import voxel_graphe, corriger_voxels_non_classes_iteratif, graphe_filtre_classes, graphe_filtre_sol, ajouter_sol, graphe_voxel
from merge import Brick


def LDRAW_Bricks(lignes, hauteur_layer_unite_LDRAW=24):
    """
    Convertit des lignes LDraw en objets Brick (merge.py).

    Paramètres
    ----------
    lignes : list of str
        Chaque ligne LDraw du type "1 <couleur> x z y 1 0 0 0 1 0 0 0 1 3005.dat"
    hauteur_layer_unite_LDRAW : int
        Hauteur d'une couche en unités LDraw (pour convertir z → layer)

    Retour
    ------
    bricks : list of Brick
        Liste d’objets Brick layer=x, x=colonne, y=ligne, length=1, width=1
    """

    bricks = []

    for line in lignes:
        if not line.startswith("1 "):
            continue  # ignorer les commentaires ou autres types
        parts = line.split()
        if len(parts) < 6:
            continue  # ligne invalide

        # Extraction des coordonnées
        x_ldraw = int(parts[2])
        z_ldraw = int(parts[3])
        y_ldraw = int(parts[4])

        # Conversion LDraw → format Brick
        layer = -z_ldraw // hauteur_layer_unite_LDRAW  # couche (inversé si z négatif)
        x = x_ldraw
        y = y_ldraw

        b = Brick(layer=layer, x=x, y=y, length=1, width=1, orientation="H")
        bricks.append(b)

    return bricks

if __name__ == "__main__":

    test_LIDAR_numpy = LIDAR_test_rectangle("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", nb_points=10000000, x_min_coin=669680.0, y_min_coin=6860143.0, longueur_x=150, longueur_y=100)
    counts, class_maj = LIDAR_couches_LEGO_LDRAW(test_LIDAR_numpy, taille_xy=1.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")

    G = voxel_graphe(counts, class_maj, densite_min=1)

    G_filtre = corriger_voxels_non_classes_iteratif(G, class_non_classe=1, classes_a_propager=[6], class_sol=2, max_iter=5)

    G_filtre = graphe_filtre_classes(G_filtre, classes_gardees=[1, 2, 3, 4, 5, 6])

    G_filtre = graphe_filtre_sol(G_filtre, class_sol=2)

    G_filtre = ajouter_sol(G_filtre, class_sol=2)

    counts, class_maj = graphe_voxel(G_filtre)

    lignes = voxel_LDRAW_classif(counts, class_maj, densite_min=1, nom_fichier="modele_echantillon_classif2.ldr")

    # Conversion en objets Brick
    bricks = LDRAW_Bricks(lignes)
    print(bricks)

