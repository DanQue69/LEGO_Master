import numpy as np

from donnees_test_LIDAR import LIDAR_test, LIDAR_test_rectangle
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_couches import LIDAR_couches, LIDAR_couches_LEGO, LIDAR_couches_LEGO_LDRAW
from LIDAR_LDRAW import voxel_LDRAW, voxel_LDRAW_classif
from LIDAR_graphe import voxel_graphe, graphe_filtre_sol, graphe_voxel



if __name__ == "__main__":

    # === IMPORT DES DONNEES ===

    # === Import des données complètes de la dalle LIDAR ===
    # file_path = "Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz"
    # las = laz_to_las(file_path)
    # LIDAR_numpy = LIDAR_numpy_utile(las)
    # counts, class_maj = LIDAR_couches_LEGO_LDRAW(LIDAR_numpy, taille_xy=1.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")

    # === Import des données échantillonnées de la dalle LIDAR ===
    # === Version échantillon aléatoire ===
    # test_LIDAR_numpy = LIDAR_test("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", nb_points=10000000, taille_zone=64)
    # counts, class_maj = LIDAR_couches_LEGO_LDRAW(test_LIDAR_numpy, taille_xy=1.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")
    # === Version échantillon rectangle ===
    test_LIDAR_numpy = LIDAR_test_rectangle("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", nb_points=10000000, x_min_coin=669680.0, y_min_coin=6860143.0, longueur_x=150, longueur_y=100)
    counts, class_maj = LIDAR_couches_LEGO_LDRAW(test_LIDAR_numpy, taille_xy=1.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")
    
    
    # === LANCEMENT DES SCRIPTS ===
    
    # === Pour les données complètes, ===
    # === Version sans classification ===
    # voxel_LDRAW(counts, densite_min=1, nom_fichier="modele_ZoneEntiere_LDRAW.ldr")
    # === Version avec classification ===
    # voxel_LDRAW_classif(counts, class_maj, densite_min=1, nom_fichier="modele_ZoneEntiere_classif.ldr")

    # === Pour les données echantilonnées, ===
    # === Version sans classification ===
    # voxel_LDRAW(counts, densite_min=3, nom_fichier="modele_echantillon_LDRAW.ldr")
    # === Version avec classification ===
    voxel_LDRAW_classif(counts, class_maj, densite_min=1, nom_fichier="modele_echantillon_classif1.ldr")

    G = voxel_graphe(counts, class_maj, densite_min=1)

    G_filtre = graphe_filtre_sol(G, class_sol=2)

    counts, class_maj = graphe_voxel(G_filtre)

    voxel_LDRAW_classif(counts, class_maj, densite_min=1, nom_fichier="modele_echantillon_classif2.ldr")

