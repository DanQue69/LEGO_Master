

class Brick:
    def __init__(self, layer, x, y, length, width, orientation="H"):
        """
        Représente une brique LEGO vue du dessus.
        (x, y) = coin inférieur-gauche en unités LEGO.
        orientation : 'H' (horizontal) ou 'V' (vertical)
        layer = couche (équivalent du Z)
        """
        self.layer = layer
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.orientation = orientation

    # -------------------------------------------------------
    # Bounding-box : retourne (x1, y1, x2, y2)
    # -------------------------------------------------------
    def bbox(self):
        """
        Retourne la boite englobante :
        x1 = x
        y1 = y
        x2 = x + length
        y2 = y + width
        """
        return (self.x, self.y,
                self.x + self.length,
                self.y + self.width)

    # -------------------------------------------------------
    # Représentation textuelle
    # -------------------------------------------------------
    def __repr__(self):
        return f"Brick(L{self.layer}, x={self.x}, y={self.y}, len={self.length}, wid={self.width}, ori={self.orientation})"


# =======================================================
#          Fonction utilitaire d'intersection
# =======================================================
def bbox_overlap(b1, b2):
    """
    Retourne True si les bounding-box se touchent ou se chevauchent.
    (zone héritée du papier LEGO : les briques adjacentes doivent
    partager une frontière pour être mergeables)
    """
    x1a, y1a, x2a, y2a = b1.bbox()
    x1b, y1b, x2b, y2b = b2.bbox()

    # Pas de chevauchement →
    if x2a <= x1b or x2b <= x1a:
        return False
    if y2a <= y1b or y2b <= y1a:
        return False

    return True


# =======================================================
#       1. are_neighbors : définition stricte du papier
# =======================================================
def are_neighbors(b1, b2):
    """
    Deux briques sont voisines si :
    - Elles sont dans la même couche
    - Leur bounding box SE TOUCHENT EXACTEMENT sur une frontière
      (pas de chevauchement diagonal, pas éloigné)

    On utilise une définition "LEGO" :
    Une jonction est vraie si une bordure entière ou partielle
    est partagée.
    """

    if b1.layer != b2.layer:
        return False

    x1a, y1a, x2a, y2a = b1.bbox()
    x1b, y1b, x2b, y2b = b2.bbox()

    # --- 1) partage d'une frontière verticale
    vertical_touch = (x2a == x1b or x2b == x1a) and not (y2a <= y1b or y2b <= y1a)

    # --- 2) partage d'une frontière horizontale
    horizontal_touch = (y2a == y1b or y2b == y1a) and not (x2a <= x1b or x2b <= x1a)

    return vertical_touch or horizontal_touch


# =======================================================
#        2. can_merge : règles géométriques
# =======================================================
def can_merge(b1, b2):
    """
    Conditions minimales pour fusionner :
    - même couche
    - même orientation (fusion horizontale ou verticale)
    - les briques doivent être parfaitement alignées
    - et adjacentes
    """

    if b1.layer != b2.layer:
        return False

    if b1.orientation != b2.orientation:
        return False

    if not are_neighbors(b1, b2):
        return False

    # Fusion horizontale
    if b1.orientation == "H":
        return (b1.y == b2.y) and (b1.width == b2.width)

    # Fusion verticale
    if b1.orientation == "V":
        return (b1.x == b2.x) and (b1.length == b2.length)

    return False


# =======================================================
#        3. merge_bricks : fusion géométrique
# =======================================================
def merge_bricks(b1, b2):
    """
    Fusionne deux briques alignées.
    Retourne une nouvelle Brick résultante.
    """

    if not can_merge(b1, b2):
        return None

    # - HORIZONTAL : les longueurs s’ajoutent
    if b1.orientation == "H":
        x = min(b1.x, b2.x)
        length = b1.length + b2.length
        return Brick(b1.layer, x, b1.y, length, b1.width, "H")

    # - VERTICAL : les hauteurs s’ajoutent
    if b1.orientation == "V":
        y = min(b1.y, b2.y)
        width = b1.width + b2.width
        return Brick(b1.layer, b1.x, y, b1.length, width, "V")


# =======================================================
#       4. get_neighbors : voisins mergeables
# =======================================================
def get_neighbors(brick, bricks):
    """
    Retourne tous les voisins mergeables d’une brique donnée.
    """

    neigh = []

    for b in bricks:
        if b is brick:
            continue
        if can_merge(brick, b):
            neigh.append(b)

    return neigh




if __name__ == "__main__":


    test_LIDAR_numpy = LIDAR_test_rectangle("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", nb_points=10000000, x_min_coin=669680.0, y_min_coin=6860143.0, longueur_x=150, longueur_y=100)
    counts, class_maj = LIDAR_couches_LEGO_LDRAW(test_LIDAR_numpy, taille_xy=4.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")

    G = voxel_graphe(counts, class_maj, densite_min=1)

    G_filtre = corriger_voxels_non_classes_iteratif(G, class_non_classe=1, classes_a_propager=[6], class_sol=2, max_iter=5)

    G_filtre = graphe_filtre_classes(G_filtre, classes_gardees=[1, 2, 3, 4, 5, 6])

    G_filtre = graphe_filtre_sol(G_filtre, class_sol=2)

    G_filtre = ajouter_sol(G_filtre, class_sol=2)

    counts, class_maj = graphe_voxel(G_filtre)

    bricks = counts_to_bricks_for_merge(counts, start_orientation="H")

    print(bricks)










