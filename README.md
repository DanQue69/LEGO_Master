# 📦 Import et Configuration du Traitement LiDAR → LEGO

## ⚠️ Important
Le traitement complet d'une dalle LiDAR peut être long.  
Il est **fortement recommandé** d’utiliser les modes d’échantillonnage afin de tester vos paramètres avant un traitement complet.

### Modes d’échantillonnage disponibles
- **`ECHANTILLON_RECTANGLE`** *(Recommandé)*  
  Extrait une zone précise définie par ses coordonnées et sa taille.
- **`ECHANTILLON_CARRE_ALEATOIRE`**  
  Sélectionne automatiquement une zone aléatoire.
- **`COMPLET`**  
  Traite l’intégralité du fichier `.laz`.

---

## 🧱 2. Géométrie des Voxels
Paramètres contrôlant la résolution et l’échelle du modèle LEGO.

- **`TAILLE_VOXEL`**  
  Résolution au sol.  
  Exemple : `1.0` = 1 mètre réel pour 1 brique LEGO.
- **`LDRAW_RATIO`**  
  Échelle verticale.  
  La valeur `1.2` correspond au ratio standard d’une brique LEGO.

---

## 🎨 3. Visualisation
Choix du rendu visuel du modèle.

- **`COULEUR`**  
  Utilise la classification LiDAR :  
  - Bâti → Gris  
  - Végétation → Vert  
  - Sol → Marron  
  - etc.
- **`GRIS`**  
  Génère une maquette monochrome de type *architecture*.

---

## ⚙️ 4. Configuration des Algorithmes
Chaque étape du pipeline peut être activée ou désactivée (`True / False`).

### 🔧 Correction des Non-Classés
Comble les trous d’information en propageant les classes voisines.

### 🧹 Filtrage
- Supprime le bruit (points flottants non connectés au sol)
- Sélectionne uniquement les classes d’intérêt (Bâti, Sol, etc.)

### 🏗️ Consolidation Structurelle (`TYPE_CONSOLIDATION`)
Définit la stratégie de solidité du modèle :

- **`PILIERS`** *(Recommandé)*  
  - Crée une coque fine pour le sol  
  - Ajoute des piliers verticaux réguliers (2×2 voxels)  
  - Bon compromis solidité / nombre de briques
- **`REMPLI`**  
  - Remplit tout le sous-sol  
  - Très solide mais coûteux en briques
- **`COQUE`**  
  - Ne conserve que la surface  
  - Économique mais fragile

### 🧱 Remplissage des Murs
Comble les trous verticaux dans les façades des bâtiments.

---

## 🗺️ 5. Export GeoTIFF (`EXPORT_IMAGES_2D`)
Si activé, le script génère une image GeoTIFF par couche de briques dans le dossier :

