"""=== Bibliothèque ==="""

import laspy


"""=== Code ==="""

# Chemin vers ton fichier .laz
file_path = "Data/LHD_FXX_0652_6863_PTS_LAMB93_IGN69.copc.laz"

# Lecture du fichier LiDAR avec le backend LASZIP
las = laspy.read(file_path, laz_backend=laspy.LazBackend.Laszip)

# Affichage du header classique
print("Header du fichier :")
print(las.header)

# Affichage du header complet
print("\nDétails du header :")
for attr in dir(las.header):
    if not attr.startswith("_") and not callable(getattr(las.header, attr)):
        print(f"{attr} : {getattr(las.header, attr)}")

# Affichage système de coordonnées
print("\nSystème de coordonnées :")
vlr_wkt = las.header.vlrs[1]  
print(vlr_wkt.string) 


# Affichage des bornes de la zone
print("\n=== Bords de la zone ===")
print("Min :", las.header.min)
print("Max :", las.header.max)

# Infos sur le système et le logiciel
print("\n=== Infos du fichier ===")
print("Système :", las.header.system_identifier)
print("Logiciel :", las.header.generating_software)


# Affichage fonction de convertion : ([X,Y,Z] * scale) + offset
print("\n=== Fonction de conversion ===")
scale = las.header.scales[0]
offset = las.header.offsets[0]
print(f"([X,Y,Z] * {scale}) + {offset}")



# Affichage du nombre de points
print("\nNombre de points :", len(las.points))



# Afficher tous les attributs disponibles pour chaque point
print("\n=== Attributs disponibles pour chaque point ===")
for attr in las.point_format.dimension_names:
    print("-", attr)



# Afficher les premières valeurs pour les n premiers points
print("\n=== Exemple des n premiers points ===")
n = int(input("Nombre de points affichés : "))
for i in range(n):
    print(f"Point {i+1} :")
    # X, Y, Z bruts et convertis
    print(f"  X brut   : {las.X[i]}   -> converti : {las.x[i]}")
    print(f"  Y brut   : {las.Y[i]}   -> converti : {las.y[i]}")
    print(f"  Z brut   : {las.Z[i]}   -> converti : {las.z[i]}")
    
    # Autres attributs
    for attr in las.point_format.dimension_names:
        if attr not in ["X", "Y", "Z"]:  # X,Y,Z déjà affichés
            print(f"  {attr} : {getattr(las, attr)[i]}")
    print()  # Ligne vide entre les points











