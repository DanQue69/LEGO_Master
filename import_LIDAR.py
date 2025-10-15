"""=== Bibliothèque ==="""

import laspy


"""=== Code ==="""

def laz_to_las(file_path):

    # Lecture du fichier LiDAR
    las = laspy.read(file_path, laz_backend=laspy.LazBackend.Laszip)

    return las
