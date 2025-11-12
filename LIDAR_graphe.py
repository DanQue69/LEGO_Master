# === Importations ===

import numpy as np
import networkx as nx

from donnees_test_LIDAR import LIDAR_test, LIDAR_test_rectangle
from import_LIDAR import laz_to_las
from LIDAR_numpy import LIDAR_numpy_utile
from LIDAR_couches import LIDAR_couches, LIDAR_couches_LEGO, LIDAR_couches_LEGO_LDRAW



# === Fonctions principales ===

def voxel_graphe(counts, class_maj, densite_min=1):
    """
    Crée un graphe 6-connexe à partir d’un modèle voxelisé LiDAR.

    Chaque voxel plein devient un nœud avec :
        - coord : position (y, x, z)
        - class_maj : classe majoritaire du voxel

    Paramètres
    ----------
    counts : np.ndarray
        Tableau 3D contenant le nombre de points LiDAR par voxel.
    class_maj : np.ndarray
        Tableau 3D des classes majoritaires par voxel.
    densite_min : int
        Seuil minimal de densité pour qu’un voxel soit considéré "plein".

    Retour
    ------
    G : networkx.Graph
        Graphe 6-connexe des voxels pleins avec attributs.
    """

    # --- Voxels pleins ---
    mask = counts >= densite_min
    coords = np.argwhere(mask)
    coord_tuples = [tuple(map(int, c)) for c in coords] 
    id_map = {coord: i for i, coord in enumerate(coord_tuples)}

    # --- Voisinage 6-connexe ---
    voisins = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    voisins_coords = (coords[:, None, :] + voisins[None, :, :]).reshape(-1, 3)

    # --- Arêtes entre voxels pleins ---
    plein_set = set(coord_tuples)
    voisin_pairs = [
        (tuple(map(int, c1)), tuple(map(int, c2)))
        for c1, c2 in zip(np.repeat(coords, 6, axis=0), voisins_coords)
        if tuple(map(int, c2)) in plein_set
    ]
    aretes = [(id_map[a], id_map[b]) for a, b in voisin_pairs]

    # --- Création du graphe ---
    G = nx.Graph()
    G.add_nodes_from(range(len(coords)))
    G.add_edges_from(aretes)

    # --- Attributs clairs ---
    nx.set_node_attributes(G, {i: (int(coords[i][1]), int(coords[i][0]), int(coords[i][2])) for i in range(len(coords))}, name='coord')
    nx.set_node_attributes(G, {i: int(class_maj[tuple(coords[i])]) for i in range(len(coords))}, name='class_maj')

    print(f"Graphe créé : {len(G.nodes())} nœuds, {len(G.edges())} arêtes.")
    return G



def graphe_filtre_sol(G, class_sol=2):
    """
    Supprime les composants du graphe non connectés à un voxel de classe 'sol'.

    Paramètres
    ----------
    G : networkx.Graph
        Graphe voxelisé.
    class_sol : int
        Code de la classe 'sol' dans la classification LIDAR.

    Retour
    ------
    G_filtre : networkx.Graph
        Graphe réduit, ne contenant que les composants connectés au sol.
    """

    # Trouver les nœuds de classe 'sol'
    nodes_sol = [n for n, d in G.nodes(data=True) if d.get('class_maj') == class_sol]

    # Identifier les composantes connexes
    composantes = list(nx.connected_components(G))

    # Garder celles qui contiennent au moins un voxel de sol
    composantes_valides = [
        c for c in composantes if any(n in nodes_sol for n in c)
    ]

    # Fusionner les composantes valides
    nodes_valides = set().union(*composantes_valides)
    G_filtre = G.subgraph(nodes_valides).copy()

    print(f"Graphe filtré : {len(G_filtre.nodes())} nœuds, {len(G_filtre.edges())} arêtes.")
    return G_filtre



def graphe_voxel(G):
    """
    Reconstruit les tableaux counts et class_maj à partir d'un graphe voxelisé.

    Les nœuds du graphe doivent avoir les attributs :
        - 'coord' : tuple (x, y, z) des indices voxel
        - 'class_maj' : classe majoritaire du voxel

    Paramètres
    ----------
    G : networkx.Graph
        Graphe voxelisé.

    Retour
    ------
    counts : np.ndarray
        Tableau 3D avec le nombre de points par voxel.
    class_maj : np.ndarray
        Tableau 3D avec la classe majoritaire de chaque voxel.
    """

    # --- Récupération des coordonnées et classes depuis le graphe ---
    coords = np.array([ (data['coord'][1], data['coord'][0], data['coord'][2])  # inverser X/Y pour cohérence
                        for _, data in G.nodes(data=True) ], dtype=int)
    classes = np.array([ data['class_maj'] for _, data in G.nodes(data=True) ], dtype=int)

    # --- Dimensions du tableau voxel ---
    ny, nx, nz = coords.max(axis=0) + 1  # +1 car indices commencent à 0

    # --- Initialisation ---
    counts = np.zeros((ny, nx, nz), dtype=int)
    class_maj = np.zeros((ny, nx, nz), dtype=int)

    # --- Remplissage ---
    for (y, x, z), c in zip(coords, classes):
        counts[y, x, z] += 1
        # Priorité : si le voxel contient déjà un autre point non-classé (1), le remplacer
        if class_maj[y, x, z] == 0 or (class_maj[y, x, z] == 1 and c != 1):
            class_maj[y, x, z] = c

    return counts, class_maj



# === Lancement du script ===

if __name__ == "__main__":

    test_LIDAR_numpy = LIDAR_test_rectangle("Data/ENSG/LHD_FXX_0669_6861_PTS_O_LAMB93_IGN69.copc.laz", nb_points=10000000, x_min_coin=669680.0, y_min_coin=6860143.0, longueur_x=150, longueur_y=100)

    counts, class_maj = LIDAR_couches_LEGO_LDRAW(test_LIDAR_numpy, taille_xy=1.0, lego_ratio=1.2, densite_min=1, prefixe_sauvegarde="layer_LEGO_LDRAW")

    G = voxel_graphe(counts, class_maj, densite_min=1)

    # Exemple : afficher les 5 premiers nœuds avec leurs coordonnées de voxel et leur classe
    for i, noeud in list(G.nodes(data=True))[:5]:
        print(i, noeud)

    G_filtre = graphe_filtre_sol(G, class_sol=2)

    # Exemple : afficher les 5 premiers nœuds avec leurs coordonnées de voxel et leur classe
    for i, noeud in list(G_filtre.nodes(data=True))[:5]:
        print(i, noeud)
