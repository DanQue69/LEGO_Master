class Brick:
    def __init__(self, layer, x, y, length, width, orientation="H"):
        self.layer = layer
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.orientation = orientation

    def bbox(self):
        return (self.x, self.y,
                self.x + self.length,
                self.y + self.width)

    def __repr__(self):
        return f"Brick(L{self.layer}, x={self.x}, y={self.y}, len={self.length}, wid={self.width}, ori={self.orientation})"


# ============================================================
#   OVERLAPS : détecter si deux briques se recouvrent
# ============================================================

def overlaps(b1, b2):
    """Retourne True si deux briques se chevauchent."""
    x1a, y1a, x2a, y2a = b1.bbox()
    x1b, y1b, x2b, y2b = b2.bbox()

    if x2a <= x1b or x2b <= x1a:
        return False
    if y2a <= y1b or y2b <= y1a:
        return False

    return True


# ============================================================
#   P1 — PERPENDICULARITY PENALTY
# ============================================================

def perpendicularity_penalty(layer_bricks, below_bricks):
    """
    Une pénalité est ajoutée si une brique est placée AU-DESSUS
    d'une brique orientée pareil.
    C’est une règle LEGO : les couches doivent alterner H / V.
    """
    penalty = 0

    for b in layer_bricks:
        for b2 in below_bricks:
            if overlaps(b, b2):
                if b.orientation == b2.orientation:
                    penalty += 1

    return penalty


# ============================================================
#   P2 — VERTICAL BOUNDARY PENALTY
# ============================================================

def vertical_boundary_penalty(layer_bricks, below_bricks):
    """
    Pénalise chaque frontière verticale visible depuis la couche du dessous.
    Une frontière verticale (joint) doit être recouverte par la couche du dessus.
    """
    penalty = 0

    # Extraire les frontières verticales des briques du dessous
    boundaries = []   # tuples (x, y_start, y_end)

    for b in below_bricks:
        x1, y1, x2, y2 = b.bbox()

        # Une brique horizontale a une frontière verticale à x2
        if b.orientation == "H":
            boundaries.append((x2, y1, y2))

        # Une brique verticale a une frontière horizontale mais on simplifie ici
        else:
            boundaries.append((x1 + b.length, y1, y2))

    # Vérifier si les briques du dessus recouvrent ces frontières
    for (bx, y1, y2) in boundaries:
        covered = False

        for b in layer_bricks:
            x1b, y1b, x2b, y2b = b.bbox()

            # Si la brique du dessus recouvre x=bx sur l’axe X
            if x1b <= bx <= x2b:
                covered = True
                break

        if not covered:
            penalty += 1

    return penalty


# ============================================================
#   P3 — HORIZONTAL T-JUNCTION PENALTY
# ============================================================

def get_T_junctions(brick, layer_bricks):
    """
    Retourne les positions x où une autre brique crée une jonction
    verticale contre cette brique (partie verticale du T).
    """
    x_juncs = []
    x1, y1, x2, y2 = brick.bbox()

    for b in layer_bricks:
        if b is brick:
            continue

        xb1, yb1, xb2, yb2 = b.bbox()

        # La jonction verticale est à xb2 si b est à gauche
        if xb2 == x1 or xb1 == x2:
            # Vérifier qu'il y a un recouvrement vertical
            if not (yb2 <= y1 or yb1 >= y2):
                x_juncs.append(xb2 if xb2 == x1 else xb1)

    return x_juncs


def horizontal_alignment_penalty(layer_bricks):
    """
    Pénalise les jonctions en T éloignées du centre de la brique.
    Plus la jonction est loin du centre → plus la structure est fragile.
    """
    penalty = 0

    for b in layer_bricks:
        x1, y1, x2, y2 = b.bbox()
        center = (x1 + x2) / 2

        for jx in get_T_junctions(b, layer_bricks):
            dist = abs(jx - center)
            penalty += dist / ((x2 - x1) ** 2)

    return penalty


# ============================================================
#   COST FUNCTION — TOTAL COST OF MODEL
# ============================================================

def cost_function(bricks, C1=1.0, C2=1.0, C3=1.0):
    """
    Calcule le coût TOTAL du modèle LEGO.
    P1 = perpendicularité entre couches
    P2 = joints verticaux non couverts
    P3 = jonctions en T mal centrées
    """

    # Rassembler par couches
    from collections import defaultdict
    layers = defaultdict(list)

    for b in bricks:
        layers[b.layer].append(b)

    total_cost = 0

    for layer in sorted(layers.keys()):
        current = layers[layer]
        below   = layers.get(layer - 1, [])

        P1 = perpendicularity_penalty(current, below)
        P2 = vertical_boundary_penalty(current, below)
        P3 = horizontal_alignment_penalty(current)

        total_cost += C1 * P1 + C2 * P2 + C3 * P3

    return total_cost
