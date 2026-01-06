# === CONFIGURATION DE L'ENVIRONNEMENT ===

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
sys.path.append(str(SRC_DIR))

try:
    from affichage_LIDAR import (afficher_bornes_zone, 
        afficher_coordonnees_systeme, 
        afficher_header, 
        afficher_infos_fichier, 
        afficher_conversion, 
        afficher_attributs_points
    )
    from import_LIDAR import laz_to_las
    from LIDAR_numpy import LIDAR_numpy_utile
    from donnees_echantillonnees_LIDAR import LIDAR_rectangle, LIDAR_carre_aleatoire
    from LIDAR_couches import LIDAR_couches_LEGO_LDRAW
    from LIDAR_LDRAW import voxel_LDRAW, voxel_LDRAW_classif
    from LIDAR_traitement import (
        voxel_graphe, 
        corriger_voxels_non_classes_iteratif, 
        graphe_filtre_classes, 
        graphe_filtre_sol,
        ajouter_sol_coque_pillier,
        ajouter_sol_coque,   
        ajouter_sol_rempli,  
        remplir_trous_verticaux, 
        graphe_voxel
    )
except ImportError as e:
    print(f"\nImpossible d'importer les modules : {e}")
    print(f"Vérifiez que le dossier 'src' contient bien tous les fichiers .py nécessaires.\n")
    sys.exit(1)



# ==========================================
# ===      PARAMÈTRES UTILISATEUR        ===
# ==========================================

# 1. FICHIER ET MODE D'IMPORT
# ---------------------------
# "AFFICHAGE_INFO_LIDAR" :          Affichage des informations du fichier LIDAR
# "COMPLET" :                       Chargement complet du fichier LIDAR
# "ECHANTILLON_CARRE_ALEATOIRE" :   Chargement d'un échantillon aléatoire en zone carrée
# "ECHANTILLON_RECTANGLE" :         Chargement d'un échantillon dans une zone rectangulaire définie
MODE_IMPORT = "ECHANTILLON_RECTANGLE"
NOM_FICHIER = "exemple.laz"

# 2. PARAMÈTRES DE VOXELISATION
# -----------------------------
TAILLE_VOXEL = 1.0    # Résolution des voxels en mètres
LDRAW_RATIO = 1.2     # Ratio de conversion LEGO (résolution/hauteur)
DENSITE_MIN = 1       # Densité minimale de points par voxel pour être pris en compte  

# 3. OPTIONS DE VISUALISATION
# -------------------------------
# "COULEUR" : Maquette avec briques colorées selon la classification LiDAR 
# "GRIS"    : Maquette monochrome (Gris standard)
VISUALISATION = "COULEUR"

# 4. CONFIGURATION DES TRAITEMENTS 
# --------------------------------------------
# Activez (True) ou désactivez (False) les étapes et réglez leurs paramètres

# A. Correction des voxels non classés 
ACTIVER_CORRECTION_NC = True
PARAM_CORRECTION = {
    "class_non_classe": 1, 
    "classes_a_propager": [6], # Propager le Bati (6) sur le non-classé
    "class_sol": 2, 
    "max_iter": 5
}

# B. Filtrage des classes 
ACTIVER_FILTRE_CLASSES = True
PARAM_FILTRE_CLASSES = {
    # 1:Non Classé, 2:Sol, 3:Végétation basse, 4:Végétation moyenne, 5:Végétation haute, 6:Bati, 9:Eau, 17:Tablier de pont, 64:Sursol pérenne, 66:Points virtuels, 67:Divers - bâtis
    "classes_gardees": [1, 2, 3, 4, 5, 6] 
}

# C. Suppression du bruit volant 
ACTIVER_FILTRE_SOL = True
PARAM_FILTRE_SOL = {
    "class_sol": 2
}

# D. Consolidation du sol 
# Choix : "PILIERS" (Recommandé), "COQUE" (Économique), "REMPLI" (Massif), "AUCUN"
TYPE_CONSOLIDATION = "PILIERS" 
PARAM_CONSOLIDATION = {
    "class_sol": 2, 
    "class_bat": 6, 
    "n_min": 2,
    "pillar_step": 4,  # Uniquement utilisé si mode PILIERS
    "pillar_width": 2  # Uniquement utilisé si mode PILIERS
}

# E. Remplissage des murs 
ACTIVER_REMPLISSAGE_MURS = True
PARAM_REMPLISSAGE = {
    "classes_batiment": [6]
}


# === EXÉCUTION PRINCIPALE ===

def exporter_modele(counts, class_maj, chemin_sortie):
    """Fonction utilitaire pour gérer le choix Couleur/Gris"""
    if VISUALISATION == "COULEUR":
        voxel_LDRAW_classif(counts, class_maj, nom_fichier=str(chemin_sortie))
    else:
        voxel_LDRAW(counts, nom_fichier=str(chemin_sortie))




if __name__ == "__main__":

    # === A. Initialisation ===
    fichier_entree = DATA_DIR / NOM_FICHIER
    
    # Création des sous-dossiers 
    dir_avant = OUTPUT_DIR / "Avant_Traitement"
    dir_apres = OUTPUT_DIR / "Apres_Traitement"
    os.makedirs(dir_avant, exist_ok=True)
    os.makedirs(dir_apres, exist_ok=True)

    if not fichier_entree.exists():
        print(f"[ERREUR] Le fichier {NOM_FICHIER} est introuvable dans {DATA_DIR}")
        sys.exit(1) 

    print(f"\n=== DÉMARRAGE DU TRAITEMENT : {NOM_FICHIER} ===")
    print(f"   Mode          : {MODE_IMPORT}")
    print(f"   Visuel        : {VISUALISATION}")



    print("\n==================================================================\n")



    # === B. Import et Chargement des Données ===
    print("1. Chargement des données...")

    if MODE_IMPORT == "AFFICHAGE_INFO_LIDAR":
        las = laz_to_las(str(fichier_entree))
        afficher_header(las)
        afficher_coordonnees_systeme(las)
        afficher_bornes_zone(las)
        afficher_infos_fichier(las)
        afficher_conversion(las)
        afficher_attributs_points(las)
        print("\nNombre total de points :", len(las.points))  
        sys.exit(0)

    elif MODE_IMPORT == "COMPLET":
        # Chargement complet
        las = laz_to_las(str(fichier_entree))
        lidar_data = LIDAR_numpy_utile(las)
        suffixe = "complet"

    elif MODE_IMPORT == "ECHANTILLON_CARRE_ALEATOIRE": 
        # Chargement échantillonné (Zone Carrée Aléatoire)
        lidar_data = LIDAR_carre_aleatoire(
            str(fichier_entree), 
            nb_points=1000000000,   # Nombre de points max à récupérer
            taille_zone=50)         # Taille de la zone carrée en mètres
        suffixe = "EchantillonCarreAleatoire"

    elif MODE_IMPORT == "ECHANTILLON_RECTANGLE": 
        # Chargement échantillonné (Zone Rectangle)
        lidar_data = LIDAR_rectangle(
            str(fichier_entree), 
            nb_points=1000000000,   # Nombre de points max à récupérer 
            x_min_coin=669680.0,    # Coordonnées du coin bas gauche du rectangle échantillonné
            y_min_coin=6860143.0,   # Coordonnées du coin bas gauche du rectangle échantillonné
            longueur_x=150,         # Longueur en x dans la direction Est-Ouest
            longueur_y=100          # Longueur en y dans la direction Nord-Sud
        )
        suffixe = "EchantillonRectangle"

    if len(lidar_data) == 0:
        print(f"[STOP] Aucun point récupéré (vérifiez les coordonnées du mode ECHANTILLON_RECTANGLE).")
        sys.exit(1)       
    print(f"   -> {len(lidar_data)} points chargés.")



    print("\n==================================================================\n")



    # === C. Voxelisation Initiale ===
    print(f"2. Voxelisation...")
    counts, class_maj = LIDAR_couches_LEGO_LDRAW(
        lidar_data, 
        taille_xy=TAILLE_VOXEL, 
        lego_ratio=LDRAW_RATIO, 
        densite_min=DENSITE_MIN
    )

    # Export visuel AVANT traitement
    print("   -> Exportation du modèle brut (Avant Traitement)...")
    nom_brut = f"{NOM_FICHIER}_modele_{suffixe}_Brut_{VISUALISATION}.ldr"
    exporter_modele(counts, class_maj, dir_avant / nom_brut)



    print("\n==================================================================\n")



    # === D. Traitements Structurels (Graphes) ===
    print("\n3. Analyse et Traitement Structurel...")
    
    # 1. Création du graphe
    G = voxel_graphe(counts, class_maj)

    # 2. Nettoyage et Filtrage 
    if ACTIVER_CORRECTION_NC:
        print("   -> Correction des voxels non classés...")
        G = corriger_voxels_non_classes_iteratif(G, **PARAM_CORRECTION)
    
    if ACTIVER_FILTRE_CLASSES:
        print("   -> Filtrage des classes indésirables...")
        G = graphe_filtre_classes(G, **PARAM_FILTRE_CLASSES)
    
    # 3. Traitements Avancés 
    if ACTIVER_FILTRE_SOL:
        print("   -> Suppression du bruit volant (Filtrage Sol)...")
        G = graphe_filtre_sol(G, **PARAM_FILTRE_SOL)
    
    # 4. Consolidation du sol 
    if TYPE_CONSOLIDATION != "AUCUN":
        print(f"   -> Consolidation du sol (Mode: {TYPE_CONSOLIDATION})...")
        
        # Récupération des paramètres communs
        p_sol = PARAM_CONSOLIDATION["class_sol"]
        p_bat = PARAM_CONSOLIDATION["class_bat"]
        p_nmin = PARAM_CONSOLIDATION["n_min"]

        if TYPE_CONSOLIDATION == "PILIERS":
            step = PARAM_CONSOLIDATION.get("pillar_step")
            pillar_width = PARAM_CONSOLIDATION.get("pillar_width")
            G = ajouter_sol_coque_pillier(G, class_sol=p_sol, class_bat=p_bat, n_min=p_nmin, pillar_step=step, pillar_width=pillar_width)
        
        elif TYPE_CONSOLIDATION == "COQUE":
            G = ajouter_sol_coque(G, class_sol=p_sol, class_bat=p_bat, n_min=p_nmin)
            
        elif TYPE_CONSOLIDATION == "REMPLI":
            G = ajouter_sol_rempli(G, class_sol=p_sol, class_bat=p_bat, n_min=p_nmin)

    # 5. Remplissage des murs 
    if ACTIVER_REMPLISSAGE_MURS:
        print("   -> Consolidation : Remplissage des murs...")
        G = remplir_trous_verticaux(G, **PARAM_REMPLISSAGE)

    # 6. Conversion inverse (Graphe -> Grille)
    counts_traite, class_maj_traite = graphe_voxel(G)



    print("\n==================================================================\n")



    # === E. Export Final ===
    print("\n4. Exportation du modèle Final...")
    nom_final = f"{NOM_FICHIER}_modele_{suffixe}_Traite_{VISUALISATION}.ldr"
    chemin_final = dir_apres / nom_final

    exporter_modele(counts_traite, class_maj_traite, chemin_final)

    print(f"\n=== TERMINÉ ===")
    print(f"1. Fichier brut   : outputs/Avant_Traitement/{nom_brut}")
    print(f"2. Fichier traité : outputs/Apres_Traitement/{nom_final}")