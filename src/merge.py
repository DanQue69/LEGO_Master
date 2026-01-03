"""
=== merge.py ===
Gestion des briques LEGO : Définition, Fusion et Contraintes physiques.
Ce module définit la classe Brick et les règles permettant de fusionner deux briques 1x1.
"""

# Catalogue simplifié des briques standard (Largeur, Longueur)
# On inclut les inverses (ex: 2x4 et 4x2) pour simplifier les tests d'existence.
# Source: Catalogue LEGO standard (Briques et Plaques utilisées comme briques)
VALID_SIZES = {
    # Briques 1.x
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 8), (1, 10), (1, 12), (1, 16),
    # Briques 2.x
    (2, 2), (2, 3), (2, 4), (2, 6), (2, 8), (2, 10),
    # Inverses pour la recherche facile
    (2, 1), (3, 1), (4, 1), (6, 1), (8, 1), (10, 1), (12, 1), (16, 1),
    (3, 2), (4, 2), (6, 2), (8, 2), (10, 2)
}

class Brick:
    def __init__(self, layer, x, y, length, width, color, orientation="H"):
        """
        Représente une brique LEGO.
        
        Paramètres
        ----------
        layer : int
            Niveau Z (couche).
        x, y : int
            Coordonnées du coin inférieur gauche sur la grille.
        length : int
            Longueur (dimension selon l'axe X si horizontal).
        width : int
            Largeur (dimension selon l'axe Y si horizontal).
        color : int
            Code couleur LDraw (ex: 0=Noir, 4=Rouge, 7=Gris).
        orientation : str
            "H" (Horizontal) ou "V" (Vertical).
        """
        self.layer = layer
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color 
        self.orientation = orientation

    def bbox(self):
        """
        Retourne la bounding box (x1, y1, x2, y2).
        x2 et y2 sont exclusifs (comme range en python).
        """
        return (self.x, self.y, self.x + self.length, self.y + self.width)

    def __repr__(self):
        return f"Brick(L{self.layer}, x={self.x}, y={self.y}, {self.length}x{self.width}, col={self.color}, ori={self.orientation})"


# =======================================================
#          Fonctions de Validation & Voisinage
# =======================================================

def is_valid_lego_part(length, width):
    """
    Vérifie si la brique existe dans le catalogue LEGO physique.
    Ex: 1x4 existe, mais 1x5 n'existe pas.
    """
    return (length, width) in VALID_SIZES

def are_neighbors(b1, b2):
    """
    Deux briques sont voisines si :
    - Elles sont dans la même couche
    - Leur bounding box SE TOUCHENT EXACTEMENT sur une frontière
      (pas de chevauchement diagonal, pas éloigné)
    """

    if b1.layer != b2.layer:
        return False

    x1a, y1a, x2a, y2a = b1.bbox()
    x1b, y1b, x2b, y2b = b2.bbox()

    # --- 1) partage d'une frontière verticale (bords X se touchent)
    # L'un finit où l'autre commence, et il y a chevauchement en Y
    vertical_touch = (x2a == x1b or x2b == x1a) and not (y2a <= y1b or y2b <= y1a)

    # --- 2) partage d'une frontière horizontale (bords Y se touchent)
    # L'un finit où l'autre commence, et il y a chevauchement en X
    horizontal_touch = (y2a == y1b or y2b == y1a) and not (x2a <= x1b or x2b <= x1a)

    return vertical_touch or horizontal_touch


# =======================================================
#        Fonctions de Fusion (Merging)
# =======================================================

def can_merge(b1, b2):
    """
    Vérifie les conditions strictes pour fusionner deux briques.
    
    Conditions :
    1. Même couche
    2. Même orientation
    3. Même couleur [IMPORTANT]
    4. Sont voisines
    5. Alignement parfait (même largeur pour fusion H, même longueur pour fusion V)
    """

    if b1.layer != b2.layer:
        return False
    
    if b1.color != b2.color: # Ajout de la contrainte couleur
        return False

    if b1.orientation != b2.orientation:
        return False

    if not are_neighbors(b1, b2):
        return False

    # Fusion horizontale (on étend X)
    if b1.orientation == "H":
        # Doivent être alignées sur Y et avoir la même hauteur (width)
        return (b1.y == b2.y) and (b1.width == b2.width)

    # Fusion verticale (on étend Y)
    if b1.orientation == "V":
        # Doivent être alignées sur X et avoir la même largeur (length)
        return (b1.x == b2.x) and (b1.length == b2.length)

    return False


def merge_bricks(b1, b2):
    """
    Fusionne deux briques SI la brique résultante est valide.
    Retourne une nouvelle instance de Brick ou None.
    """

    if not can_merge(b1, b2):
        return None

    new_brick = None

    # - Cas HORIZONTAL : les longueurs s’ajoutent
    if b1.orientation == "H":
        x = min(b1.x, b2.x)
        length = b1.length + b2.length
        
        # Vérification inventaire AVANT de valider la fusion
        if is_valid_lego_part(length, b1.width):
            new_brick = Brick(b1.layer, x, b1.y, length, b1.width, b1.color, "H")

    # - Cas VERTICAL : les largeurs s’ajoutent (conceptuellement pour nous width augmente en Y)
    elif b1.orientation == "V":
        y = min(b1.y, b2.y)
        width = b1.width + b2.width
        
        # Vérification inventaire
        if is_valid_lego_part(b1.length, width):
            new_brick = Brick(b1.layer, b1.x, y, b1.length, width, b1.color, "V")

    return new_brick


def get_neighbors(brick, bricks):
    """
    Retourne tous les voisins mergeables d’une brique donnée dans une liste.
    Note : Cette fonction est linéaire O(N), pour l'optimisation on préférera
    passer par une grille spatiale (voir cost_func_change.py).
    """
    neigh = []
    for b in bricks:
        if b is brick:
            continue
        if can_merge(brick, b):
            neigh.append(b)
    return neigh