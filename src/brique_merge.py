


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

from merge import Brick

# === Paramètres de conversion LDraw ===
SCALE_XY = 20.0
SCALE_Z = 24.0

# === Mapping Couleurs (LIDAR -> LEGO) ===

# # === Dictionnaire classification LIDAR en couleur LDraw hexadécimal (Direct Color) ===
# # Décommenter si besoin de correspondance visuelle stricte.
# LIDAR_TO_LEGO_COLORS_HEX = {
#     1: 0x2000000,   # Non classé => noir
#     2: 0x28B4513,   # Sol => marron
#     3: 0x290EE90,   # Végétation basse  => vert clair
#     4: 0x2008000,   # Végétation moyenne => vert
#     5: 0x200561B,   # Végétation haute => vert foncé
#     6: 0x2555555,   # Bâtiment => gris
#     9: 0x20000FF,   # Eau => bleu
#     17:0x2FF0000,   # Tablier de pont => rouge 
#     64:0x2FFA500,   # Sursol => orange
#     66:0x2FFFFFF,   # Points virtuels => blanc
#     67:0x2FFFF00,   # Divers bâtis => jaune
# }

# === Dictionnaire classification LIDAR en couleur LDraw classique (Codes entiers) ===
# Correspond aux couleurs standard de la palette LDraw et aux briques réelles LEGO.
LIDAR_TO_LEGO_COLORS = {
    1: 0,   # Non classé → Noir
    2: 6,   # Sol → Brun
    3: 10,  # Végétation basse → Vert vif
    4: 2,   # Végétation moyenne → Vert
    5: 288, # Végétation haute → Vert sapin 
    6: 7,   # Bâtiment → Gris clair 
    9: 1,   # Eau → Bleu
    17: 4,  # Pont → Rouge
    64: 14, # Sursol → Jaune
    66: 15, # Virtuels → Blanc
    67: 8,  # Divers bâtis → Gris foncé 
}

# si VISUALISATION = "GRIS"
DEFAULT_GRAY = 16 


def bricks_from_ldr(lignes):
    """
    Convertit des lignes LDraw en objets Brick en corrigeant l'échelle.
    Gère les coordonnées et la couleur.
    """
    bricks = []

    for line in lignes:
        parts = line.strip().split()
        
        # Format LDraw : 1 <couleur> <x> <z_hauteur> <y> ...
        if not parts or parts[0] != "1" or len(parts) < 5:
            continue

        try:
            color_code = int(parts[1])
            x_ldr = float(parts[2])
            z_ldr_hauteur = float(parts[3]) 
            y_ldr = float(parts[4])

            # Conversion inverse (LDraw -> Grille Voxel 1x1)
            # x_ldr = ix * 20
            ix = int(round(x_ldr / SCALE_XY))
            # y_ldr = iy * 20
            iy = int(round(y_ldr / SCALE_XY))
            # z_ldr = -iz * 24
            iz = int(round(-z_ldr_hauteur / SCALE_Z))

            b = Brick(
                layer=iz, 
                x=ix, 
                y=iy, 
                length=1, 
                width=1, 
                color=color_code, 
                orientation="H"
            )
            bricks.append(b)

        except ValueError:
            continue

    return bricks


def bricks_from_numpy(counts, class_maj=None, visualisation="COULEUR"):
    """
    Convertit les tableaux NumPy (voxels) en objets Brick.
    
    Paramètres
    ----------
    visualisation : str
        "COULEUR" => utilise la classification LIDAR mappée vers LEGO.
        "GRIS"    => utilise DEFAULT_GRAY (16).
    """
    bricks = []
    indices = np.argwhere(counts > 0)
    
    for iy, ix, iz in indices:
        
        lego_color = DEFAULT_GRAY

        # Gestion de la couleur
        if visualisation == "COULEUR" and class_maj is not None:
            c_lidar = class_maj[iy, ix, iz]
            # On récupère la couleur standard, ou le gris 16 par défaut si classe inconnue
            lego_color = LIDAR_TO_LEGO_COLORS.get(c_lidar, DEFAULT_GRAY)
        
        # Création de la brique unitaire
        b = Brick(
            layer=iz,
            x=ix,
            y=iy,
            length=1,
            width=1,
            color=lego_color,
            orientation="H"
        )
        bricks.append(b)

    return bricks