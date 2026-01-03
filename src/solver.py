"""
=== solver.py ===
Algorithme d'optimisation pour fusionner les briques LEGO.
Approche : Glouton Alterné (Alternating Greedy).
"""
# === Importations ===
import sys
import os
import numpy as np
from pathlib import Path

# --- Configuration des chemins ---
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

sys.path.append(str(SRC_DIR))

# --- Imports des modules du projet ---
from donnees_echantillonnees_LIDAR import LIDAR_carre_aleatoire, LIDAR_rectangle
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_couches import LIDAR_couches, LIDAR_couches_LEGO, LIDAR_couches_LEGO_LDRAW
from LIDAR_LDRAW import voxel_LDRAW, voxel_LDRAW_classif

from merge import Brick
from collections import defaultdict
from merge import merge_bricks
from cost_function import total_cost_function



# =============================================================================
# CATALOGUE DE PIÈCES LDRAW
# Mapping (Largeur, Longueur) -> Fichier .dat
# Note : Toujours mettre la plus petite dimension en premier dans la clé (min, max)
# =============================================================================
LEGO_PARTS = {
    # --- Briques 1.x ---
    (1, 1): "3005.dat",  # Brick 1 x 1
    (1, 2): "3004.dat",  # Brick 1 x 2
    (1, 3): "3622.dat",  # Brick 1 x 3
    (1, 4): "3010.dat",  # Brick 1 x 4
    (1, 6): "3009.dat",  # Brick 1 x 6
    (1, 8): "3008.dat",  # Brick 1 x 8
    (1, 10): "6111.dat", # Brick 1 x 10
    (1, 12): "6112.dat", # Brick 1 x 12
    (1, 16): "2465.dat", # Brick 1 x 16
    
    # --- Briques 2.x ---
    (2, 2): "3003.dat",  # Brick 2 x 2
    (2, 3): "3002.dat",  # Brick 2 x 3
    (2, 4): "3001.dat",  # Brick 2 x 4
    (2, 6): "2456.dat",  # Brick 2 x 6
    (2, 8): "3007.dat",  # Brick 2 x 8
    (2, 10): "3006.dat", # Brick 2 x 10
}


def print_brick_stats(bricks):
    """
    Affiche le décompte des briques par type (Inventaire).
    """
    stats = Counter()
    
    for b in bricks:
        # On normalise les dimensions (petit x grand) pour que 2x4 et 4x2 soient comptés ensemble
        dims = tuple(sorted((b.width, b.length)))
        stats[dims] += 1
        
    print("\n" + "="*40)
    print("      INVENTAIRE FINAL (BOM)      ")
    print("="*40)
    print(f"{'TYPE':<15} | {'REF LDRAW':<10} | {'QTÉ':<5}")
    print("-" * 36)
    
    # Tri par largeur puis longueur pour l'affichage
    sorted_keys = sorted(stats.keys())
    
    total_bricks = 0
    
    for (w, l) in sorted_keys:
        count = stats[(w, l)]
        total_bricks += count
        
        # Récupération de la référence LDraw
        ref = LEGO_PARTS.get((w, l), "CUSTOM")
        
        label = f"{w} x {l}"
        print(f"{label:<15} | {ref:<10} | {count:<5}")
        
    print("-" * 36)
    print(f"{'TOTAL':<15} | {'':<10} | {total_bricks:<5}")
    print("="*40 + "\n")


def export_to_ldr(bricks, filename):
    """
    Génère le fichier .ldr final.
    - Si la brique existe dans LEGO_PARTS, utilise le vrai fichier .dat (avec rotation si besoin).
    - Sinon, utilise une brique 1x1 étirée (méthode fallback).
    """
    header = [
        "0 Optimized LEGO Model\n",
        "0 Name: " + str(filename) + "\n",
        "0 Author: Solver Algo Greedy\n"
    ]
    
    lines = []
    
    # Facteurs d'échelle LDraw
    LDR_UNIT = 20.0
    LDR_HEIGHT = 24.0

    for b in bricks:
        # 1. Calcul du centre géométrique (Position)
        # ------------------------------------------
        # Coin de la brique en unités LDraw
        x_coin = b.x * LDR_UNIT
        y_coin = b.y * LDR_UNIT
        z_pos = -b.layer * LDR_HEIGHT 

        # Dimensions réelles
        dim_x = b.length * LDR_UNIT
        dim_y = b.width * LDR_UNIT

        # Le centre pour LDraw est : Coin + Demi-Dimension - Demi-Stud(10)
        center_x = x_coin + (dim_x / 2.0) - 10.0
        center_y = y_coin + (dim_y / 2.0) - 10.0

        # 2. Identification de la pièce
        # -----------------------------
        # On trie (largeur, longueur) pour matcher le dictionnaire (min, max)
        dims_sorted = tuple(sorted((b.width, b.length)))
        part_file = LEGO_PARTS.get(dims_sorted)

        if part_file:
            # === CAS A : PIÈCE RÉELLE EXISTANTE ===
            
            # Gestion de la Rotation (Orientation)
            # Par défaut, les pièces LDraw ont leur longueur alignée sur X.
            
            # Matrice d'identité (Pas de rotation)
            # 1 0 0 | 0 1 0 | 0 0 1
            a, b_rot, c, d, e, f, g, h, i = 1, 0, 0, 0, 1, 0, 0, 0, 1

            need_rotation = False
            
            # Si c'est une pièce carrée (2x2, 1x1), l'orientation importe peu géométriquement
            if b.length == b.width:
                pass 
            
            # Si orientation = 'V' (Vertical dans la grille NumPy = Axe Y)
            # Alors que la pièce LDraw par défaut est allongée sur X.
            elif b.orientation == "V":
                need_rotation = True

            if need_rotation:
                # Rotation 90 degrés autour de l'axe Y (Vertical LDraw)
                # X -> Z, Z -> -X
                # Matrice : 0 0 -1 | 0 1 0 | 1 0 0
                a, b_rot, c = 0, 0, 1
                d, e, f     = 0, 1, 0
                g, h, i     = -1, 0, 0

            line = f"1 {b.color} {center_x:.2f} {z_pos:.2f} {center_y:.2f} {a} {b_rot} {c} {d} {e} {f} {g} {h} {i} {part_file}\n"
        
        else:
            # === CAS B : PIÈCE INCONNUE (FALLBACK) ===
            # On utilise la méthode d'étirement sur une 3005.dat (1x1)
            
            mat_a = b.length
            mat_e = 1 
            mat_i = b.width
            
            # On remet le scale matrix simple
            line = f"1 {b.color} {center_x:.2f} {z_pos:.2f} {center_y:.2f} {mat_a} 0 0 0 {mat_e} 0 0 0 {mat_i} 3005.dat\n"

        lines.append(line)

    with open(filename, "w") as f:
        f.writelines(header)
        f.writelines(lines)
    
    print(f"[Export] Fichier généré : {filename} ({len(bricks)} briques)")


def optimize_layer_1d(bricks, orientation):
    """
    Fusionne les briques d'une couche dans une direction donnée (H ou V).
    """
    # 1. Tri intelligent des briques
    if orientation == "H":
        # Pour fusionner horizontalement (------), on parcourt ligne par ligne (Y), puis colonne (X)
        bricks.sort(key=lambda b: (b.y, b.x))
        # On force l'orientation voulue pour tenter la fusion
        for b in bricks: b.orientation = "H"
            
    else: # Vertical
        # Pour fusionner verticalement (|), on parcourt colonne par colonne (X), puis ligne (Y)
        bricks.sort(key=lambda b: (b.x, b.y))
        for b in bricks: b.orientation = "V"
    
    merged_list = []
    
    if not bricks:
        return []

    # Algorithme Glouton (Greedy)
    current_brick = bricks[0]
    
    for next_brick in bricks[1:]:
        # On tente de fusionner la courante avec la suivante
        merged = merge_bricks(current_brick, next_brick)
        
        if merged:
            # SUCCÈS : La brique grandit, on continue avec elle
            current_brick = merged
        else:
            # ÉCHEC : La brique est finie (rupture couleur, géométrie ou inventaire)
            merged_list.append(current_brick)
            current_brick = next_brick # On passe à la suivante
            
    # Ne pas oublier la dernière brique
    merged_list.append(current_brick)
    
    return merged_list


def solve_greedy_stripe(bricks):
    """
    Stratégie principale : Rayures (Stripes).
    - Couches paires : Fusion Horizontale.
    - Couches impaires : Fusion Verticale.
    """
    print(f"[Solver] Démarrage... ({len(bricks)} briques initiales)")


    # 1. Regrouper par couches
    layers = defaultdict(list)
    for b in bricks:
        layers[b.layer].append(b)
    
    final_bricks = []
    
    # 2. Traiter chaque couche
    sorted_layer_indices = sorted(layers.keys())
    
    for layer_idx in sorted_layer_indices:
        layer_content = layers[layer_idx]
        
        # Déterminer la direction de fusion
        if layer_idx % 2 == 0:
            target_orientation = "H"
        else:
            target_orientation = "V"

        # 3. Optimisation de la couche
        optimized_layer = optimize_layer_1d(layer_content, target_orientation)
        final_bricks.extend(optimized_layer)

    
    # Statistiques
    reduction = 100 * (1 - len(final_bricks) / len(bricks))
    print(f"[Solver] Briques : {len(bricks)} -> {len(final_bricks)} (Réduction : {reduction:.1f}%)")
    
    return final_bricks



if __name__ == "__main__":
    import time
    
    # === IMPORTS POUR LE TEST UNIQUEMENT ===
    try:
        # On essaie d'importer la factory. 
        # ATTENTION : Renomme ton fichier 'brique_merge.py' en 'brick_factory.py'
        from brick_factory import bricks_from_numpy
    except ImportError:
        # Fallback si tu n'as pas renommé
        try:
            from brique_merge import bricks_from_numpy
        except ImportError:
            print("ERREUR CRITIQUE : Impossible d'importer 'bricks_from_numpy'.")
            print("Vérifiez que 'brick_factory.py' (ou brique_merge.py) est dans 'src'.")
            sys.exit(1)

    from donnees_echantillonnees_LIDAR import LIDAR_rectangle
    from LIDAR_couches import LIDAR_couches_LEGO_LDRAW

    print("\n=== LANCEMENT DU TEST UNITAIRE : SOLVER.PY ===\n")

    # 1. GÉNÉRATION DE DONNÉES LIDAR (Simulation)
    # -------------------------------------------
    nom_fichier = "exemple.laz" # Ou "exemple.laz"
    file_path = DATA_DIR / nom_fichier
    
    if not file_path.exists():
        print(f"[ERREUR] Fichier {nom_fichier} introuvable pour le test.")
        sys.exit(1)

    print(f"1. Chargement et Voxelisation de {nom_fichier}...")
    # On prend une petite zone pour que le test soit rapide (ex: 40x40m)
    lidar_data = LIDAR_rectangle(
        file_path, 
        nb_points=1000000000,   # Nombre de points max à récupérer 
        x_min_coin=669680.0,    # Coordonnées du coin bas gauche du rectangle échantillonné
        y_min_coin=6860143.0,   # Coordonnées du coin bas gauche du rectangle échantillonné
        longueur_x=150,         # Longueur en x dans la direction Est-Ouest
        longueur_y=100          # Longueur en y dans la direction Nord-Sud 
    )

    # Voxelisation (Step classique)
    counts, class_maj = LIDAR_couches_LEGO_LDRAW(
        lidar_data, 
        taille_xy=1.0, 
        lego_ratio=1.2, 
        densite_min=1
    )
    print(f"   -> Grille obtenue : {counts.shape}")

    # 2. CONVERSION EN BRIQUES 1x1
    # ----------------------------
    print("\n2. Conversion Numpy -> Objets Brick (Non optimisés)...")
    # On utilise le mode COULEUR pour tester la contrainte de couleur lors du merge
    raw_bricks = bricks_from_numpy(counts, class_maj, visualisation="COULEUR")
    print(f"   -> {len(raw_bricks)} briques 1x1 générées.")

    # 3. CALCUL DU COÛT INITIAL
    # -------------------------
    print("\n3. Évaluation Structurelle Initiale...")
    # Attention : total_cost_function peut être long sur >100k briques.
    # Pour le test, on le lance.
    t_start = time.time()
    cout_init = total_cost_function(raw_bricks)
    print(f"   -> Coût Initial : {cout_init:.2f} (Calculé en {time.time()-t_start:.2f}s)")
    print("      (Note : Un coût élevé est normal car les murs verticaux ne sont pas croisés)")

    # 4. OPTIMISATION (LE SOLVER)
    # ---------------------------
    print("\n4. Exécution du Solver (Greedy Stripe)...")
    optimized_bricks = solve_greedy_stripe(raw_bricks)

    # 5. CALCUL DU COÛT FINAL
    # -----------------------
    print("\n5. Évaluation Structurelle Finale...")
    cout_final = total_cost_function(optimized_bricks)
    print(f"   -> Coût Final : {cout_final:.2f}")
    
    gain = cout_init - cout_final
    print(f"   -> Gain de solidité : {gain:.2f}")

    # 6. EXPORT
    # ---------
    print("\n6. Exportation du résultat...")
    nom_sortie = OUTPUT_DIR / "Test_Solver_Resultat.ldr"
    export_to_ldr(optimized_bricks, str(nom_sortie))
    
    print(f"\n=== TEST TERMINÉ ===")
    print(f"Fichier de sortie : {nom_sortie}")