import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random
from PIL import Image

# Définition de la taille de la carte en hauteur et en largeur
largeur = 300
hauteur = 300

# Définition de l'échelle du bruit (affecte le niveau de détail)
echelle = 150.0

# Définition d'une graine aléatoire pour la génération du bruit
graine = random.randint(0, 1000000)
random.seed(graine)
np.random.seed(graine)

# Génération de la carte de hauteur en utilisant le bruit de Perlin
carte_hauteur = np.zeros((largeur, hauteur))
for i in range(largeur):
    for j in range(hauteur):
        carte_hauteur[i][j] = snoise2(i/echelle, j/echelle, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=graine)

# Normalisation des valeurs dans la plage [0, 1]
carte_hauteur = (carte_hauteur - np.min(carte_hauteur)) / (np.max(carte_hauteur) - np.min(carte_hauteur))

# Génération d'une carte pour les zones d'eau, de plaines, de forêts et de montagnes
carte_eau = carte_hauteur < 0.35  # Réglage du seuil pour les zones d'eau
carte_plaine = (carte_hauteur >= 0.35) & (carte_hauteur < 0.525)  # Zones de plaines
carte_foret = (carte_hauteur >= 0.4) & (carte_hauteur < 0.65)  # Zones de forêts
carte_montagne = carte_hauteur >= 0.65  # Zones de montagnes

# Définition des gradients de couleur en fonction de l'élévation
couleurs = [
    (0, 0, 0.5),    # Eau profonde
    (0, 0, 1),      # Eau peu profonde
    (0.8, 0.8, 0.2),# Plage
    (0.2, 0.8, 0.2),# Plaine (vert clair)
    (0, 0.5, 0),     # Forêt (vert foncé)
    (0.3, 0.2, 0.1),  # Montagne (marron foncé)
    (1, 1, 1)        # Neige (blanc)
]

# Interpolation des couleurs en fonction de l'élévation
def interpoler_couleur(valeur, carte_couleur):
    valeur = max(0, min(1, valeur))
    index = int(valeur * (len(carte_couleur) - 1))
    return np.array(carte_couleur[index])

# Génération de la carte de couleur
carte_couleur = np.zeros((largeur, hauteur, 3))
for i in range(largeur):
    for j in range(hauteur):
        if carte_eau[i][j]:  # Si c'est de l'eau
            carte_couleur[i][j] = interpoler_couleur(carte_hauteur[i][j], [couleurs[0], couleurs[1]])  # Choix des couleurs d'eau profonde ou peu profonde
        elif carte_plaine[i][j]:  # Si c'est une plaine
            carte_couleur[i][j] = couleurs[3]  # Vert clair pour les plaines
        elif carte_foret[i][j]:  # Si c'est une forêt
            carte_couleur[i][j] = couleurs[4]  # Vert foncé pour les forêts
        elif carte_montagne[i][j]:  # Si c'est une montagne
            carte_couleur[i][j] = couleurs[5]  # Marron foncé pour les montagnes
            if carte_hauteur[i][j] > 0.85:  # Ajoutez de la neige pour les zones de montagnes élevées
                carte_couleur[i][j] = couleurs[6]  # Neige

# Ajout des plages autour des zones d'eau
masque_eau_erode = np.pad(carte_eau, 1, mode='constant', constant_values=True)  # Ajout d'une bordure d'eau pour éviter les problèmes de bords
masque_eau_erode = masque_eau_erode[:-2, :-2] | masque_eau_erode[1:-1, :-2] | masque_eau_erode[2:, :-2] | masque_eau_erode[:-2, 1:-1] | masque_eau_erode[2:, 1:-1] | masque_eau_erode[:-2, 2:] | masque_eau_erode[1:-1, 2:] | masque_eau_erode[2:, 2:]  # Érosion de l'eau sur les bords
carte_plage = masque_eau_erode & carte_plaine  # Intersection de l'eau érodée avec les zones de plaine
carte_couleur[carte_plage] = interpoler_couleur(0.5, [couleurs[2], couleurs[3]])  # Coloration des plages

# Noms de villes vikings aléatoires
noms_villes_vikings = ["Asgard", "Valhalla", "Niflheim", "Midgard", "Jotunheim", "Helheim", "Svartalfheim", "Alfheim", "Vanaheim", "Muspelheim", "Yggdrasil", "Ragnarok", "Bifrost", "Fenrir", "Nidavellir"]

# Génération de coordonnées et de noms de villes aléatoires
nb_villes = 10
coordonnees_villes = set()  # Utilisation d'un ensemble pour stocker les coordonnées des villes
noms_villes = []

while len(coordonnees_villes) < nb_villes:
    x, y = np.random.randint(10, largeur-10), np.random.randint(10, hauteur-10)  # Assure que les villes ne se situent pas trop près des bords de la carte
    if carte_plaine[x, y] and (x, y) not in coordonnees_villes:  # Vérification si la ville est sur une plaine et n'est pas déjà dans la liste
        if not np.any(carte_eau[x - 15:x + 16, y - 15:y + 16]):  # vérification si la ville n'est pas trop proche de l'eau
            coordonnees_villes.add((x, y))
            nom_ville = random.choice(noms_villes_vikings)
            noms_villes_vikings.remove(nom_ville)  # Supprimer le nom de ville utilisé pour éviter les répétitions
            noms_villes.append(nom_ville)

# Espacement des villes
coordonnees_villes_esp = []
for coordonnee in coordonnees_villes:
    x, y = coordonnee
    dx, dy = 0, 0
    while any(np.linalg.norm(np.array((x+dx, y+dy)) - np.array(other)) < 30 for other in coordonnees_villes_esp):
        dx += random.randint(-50, 50)
        dy += random.randint(-50, 50)
    coordonnees_villes_esp.append((x+dx, y+dy))

# Sites historiques
sites_historiques = {
    "Ruines de Valhalla": None,
    "Bataille de Ragnarok": None,
    "Tombe de Yggdrasil": None,
}
# Attribution des coordonnées aléatoires aux sites historiques
for nom_site in sites_historiques:
    x, y = np.random.randint(20, largeur-20), np.random.randint(20, hauteur-20)
    while not carte_plaine[x, y]:
        x, y = np.random.randint(20, largeur-20), np.random.randint(20, hauteur-20)
    sites_historiques[nom_site] = (x, y)

# Génération de la carte avec les sites historiques
for nom_site, coordonnee_site in sites_historiques.items():
    x, y = coordonnee_site
    carte_couleur[x, y] = (1, 0, 0)  # Couleur des sites historiques

# Ajout de l'image de hache pour la bataille de Ragnarok
if "Bataille de Ragnarok" in sites_historiques:
    x, y = sites_historiques["Bataille de Ragnarok"]
    image_hache = Image.open("/Users/mathieusin/revision_exam/hache.png")  # Ouvrir l'image de hache
    taille_zone = (31,31)
    image_hache = image_hache.resize(taille_zone)  # Redimensionner l'image de hache
    image_hache = np.array(image_hache)  # Convertir l'image de hache en tableau NumPy
    carte_couleur[x-15:x+16, y-15:y+16] = image_hache  # Coller l'image de hache sur la carte

# Affichage de la carte de hauteur colorée en 2D avec zoom et déplacement activés
fig, ax = plt.subplots(figsize=(8, 6))  # Définition de la taille de la figure
im = ax.imshow(carte_couleur, origin='lower')
ax.axis('off')  # Suppression des indications d'échelle sur les côtés

# Ajout des points noirs pour marquer les emplacements des villes
for coordonnee_ville, nom_ville in zip(coordonnees_villes_esp, noms_villes):
    x, y = coordonnee_ville
    if 0 <= x < largeur and 0 <= y < hauteur:  # Vérification que les coordonnées de la ville sont dans les limites de la carte
        ax.plot(y, x, marker='o', markersize=7, color='black')  # Ajout du point noir pour marquer la ville
        ax.text(y, x + 7, nom_ville, color='black', fontsize=10, ha='center', va='center', fontfamily='cursive')  # Ajout du nom de la ville au-dessus du point avec la police cursive

# Ajout des points rouges pour marquer les emplacements des sites historiques
for nom_site, coordonnee_site in sites_historiques.items():
    x, y = coordonnee_site
    if 0 <= x < largeur and 0 <= y < hauteur:  # Vérification que les coordonnées du site historique sont dans les limites de la carte
        ax.plot(y, x, marker='o', markersize=5, color='red')  # Ajout du point rouge pour marquer le site historique avec une taille de point plus grande
        ax.text(y, x + 7, nom_site, color='red', fontsize=8, ha='center', va='center', fontfamily='cursive')  # Ajout du nom du site historique au-dessus du point avec la police cursive

# Légende
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Villes'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Sites historiques'),
    plt.Line2D([0], [0], color='blue', linewidth=3, label='Eau'),
    plt.Line2D([0], [0], color='green', linewidth=3, label='Plaine'),
    plt.Line2D([0], [0], color='darkgreen', linewidth=3, label='Forêt'),  # Ajout de la légende pour les forêts
    plt.Line2D([0], [0], color='yellow', linewidth=3, label='Plage'),
    plt.Line2D([0], [0], color='brown', linewidth=3, label='Montagne'),
    plt.Line2D([0], [0], color='white', linewidth=3, label='Neige')  # Ajout de la légende pour la neige
]

# Ajout de la légende en dehors de la carte
fig.subplots_adjust(right=0.9)  # Ajustement des marges pour laisser de l'espace à la légende
ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(-0.38, 0.8))

# Echelle de couleur pour représenter l'altitude
cax = fig.add_axes([0.8, 0.1, 0.03, 0.8])  # Définition de la position et de la taille de l'échelle de couleur
norm = plt.Normalize(vmin=0, vmax=2)  # Normalisation de l'altitude entre 0 et 2
cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='terrain'), cax=cax)  # Ajout de l'échelle de couleur
cbar.set_label('Altitude')  # Ajout du label à l'échelle de couleur
cbar.set_ticks([2, 0.8, 0.6, 0.4, 0.2, 0])  # Définition des valeurs de l'altitude pour les étiquettes



plt.show()