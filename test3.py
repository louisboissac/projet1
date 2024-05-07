import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random

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

# Génération d'une carte pour les zones d'eau et de terre
carte_eau = carte_hauteur < 0.3  # Réglage du seuil pour les zones d'eau
carte_terre = carte_hauteur >= 0.3  # Zones de terre

# Définition des gradients de couleur en fonction de l'élévation
couleurs = [
    (0, 0, 0.5),    # Eau profonde
    (0, 0, 1),      # Eau peu profonde
    (0.8, 0.8, 0.2),# Plage
    (0.2, 0.8, 0.2),# Terre
    (0.3, 0.2, 0.1),# Montagne (marron foncé)
    (1, 1, 1)       # Neige
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
        else:  # Si c'est de la terre
            carte_couleur[i][j] = interpoler_couleur(carte_hauteur[i][j], [couleurs[3], couleurs[4], couleurs[5]])  # Choix des couleurs de terre, montagne ou neige

# Ajout des plages autour des zones d'eau
masque_eau_erode = np.pad(carte_eau, 1, mode='constant', constant_values=True)  # Ajout d'une bordure d'eau pour éviter les problèmes de bords
masque_eau_erode = masque_eau_erode[:-2, :-2] | masque_eau_erode[1:-1, :-2] | masque_eau_erode[2:, :-2] | masque_eau_erode[:-2, 1:-1] | masque_eau_erode[2:, 1:-1] | masque_eau_erode[:-2, 2:] | masque_eau_erode[1:-1, 2:] | masque_eau_erode[2:, 2:]  # Érosion de l'eau sur les bords
carte_plage = masque_eau_erode & carte_terre  # Intersection de l'eau érodée avec les zones de terre
carte_couleur[carte_plage] = interpoler_couleur(0.5, [couleurs[2], couleurs[3]])  # Coloration des plages

# Ajout de la neige sur les sommets des montagnes
carte_neige = carte_hauteur > 0.8  # Réglage du seuil pour les sommets de montagne
carte_couleur[carte_neige] = (1, 1, 1)  # Couleur de la neige

# Noms de villes vikings aléatoires
noms_villes_vikings = ["Asgard", "Valhalla", "Niflheim", "Midgard", "Jotunheim", "Helheim", "Svartalfheim", "Alfheim", "Vanaheim", "Muspelheim", "Yggdrasil", "Ragnarok", "Bifrost", "Fenrir", "Nidavellir"]

# Génération de coordonnées et de noms de villes aléatoires
nb_villes = 10
coordonnees_villes = set()  # Utilisation d'un ensemble pour stocker les coordonnées des villes
noms_villes = []

while len(coordonnees_villes) < nb_villes:
    x, y = np.random.randint(20, largeur-20), np.random.randint(20, hauteur-20)  # Assure que les villes ne se situent pas trop près des bords de la carte
    if carte_terre[x, y] and (x, y) not in coordonnees_villes:  # Vérification si la ville est sur la terre et n'est pas déjà dans la liste
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
    "Tombe de Yggdrasil": None
}

# Attribution des coordonnées aléatoires aux sites historiques
for nom_site in sites_historiques:
    x, y = np.random.randint(20, largeur-20), np.random.randint(20, hauteur-20)
    while not carte_terre[x, y]:
        x, y = np.random.randint(20, largeur-20), np.random.randint(20, hauteur-20)
    sites_historiques[nom_site] = (x, y)

# Génération de la carte avec les sites historiques
for nom_site, coordonnee_site in sites_historiques.items():
    x, y = coordonnee_site
    carte_couleur[x, y] = (1, 0, 0)  # Couleur des sites historiques

# Affichage de la carte de hauteur colorée en 2D avec zoom et déplacement activés
plt.figure(figsize=(8, 6))  # Définition de la taille de la figure
plt.imshow(carte_couleur, origin='lower')
plt.axis('off')  # Suppression des indications d'échelle sur les côtés

# Ajout des points noirs pour marquer les emplacements des villes
for coordonnee_ville, nom_ville in zip(coordonnees_villes_esp, noms_villes):
    x, y = coordonnee_ville
    plt.plot(y, x, marker='o', markersize=8, color='black')  # Ajout du point noir pour marquer la ville
    plt.text(y, x + 7, nom_ville, color='black', fontsize=12, ha='center', va='center', fontfamily='cursive')  # Ajout du nom de la ville au-dessus du point avec la police cursive

# Ajout des points rouges pour marquer les emplacements des sites historiques
for nom_site, coordonnee_site in sites_historiques.items():
    x, y = coordonnee_site
    plt.plot(y, x, marker='o', markersize=7, color='red')  # Ajout du point rouge pour marquer le site historique avec une taille de point plus grande
    plt.text(y, x + 7, nom_site, color='red', fontsize=7, ha='center', va='center', fontfamily='cursive')  # Ajout du nom du site historique au-dessus du point avec la police cursive

plt.show()
