import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random
import mplcursors

# Définition de la taille de la carte en hauteur et en largeur
largeur = 200
hauteur = 200

# Définition de l'échelle du bruit (affecte le niveau de détail)
echelle = 125.0

# Définition d'une graine aléatoire pour la génération du bruit
graine = random.randint(0, 1000000)
random.seed(graine)
np.random.seed(graine)

# Génération de la carte de hauteur en utilisant le bruit de Perlin
carte_hauteur = np.zeros((largeur, hauteur))
for i in range(largeur):
    for j in range(hauteur):
        carte_hauteur[i][j] = snoise2(i / echelle, j / echelle, octaves=6, persistence=0.5, lacunarity=2.0,
                                      repeatx=1024, repeaty=1024, base=graine)

# Normalisation des valeurs dans la plage [0, 1]
carte_hauteur = (carte_hauteur - np.min(carte_hauteur)) / (np.max(carte_hauteur) - np.min(carte_hauteur))

# Génération d'une carte pour les zones d'eau et de terre
carte_eau = carte_hauteur < 0.3  # Réglage du seuil pour les zones d'eau
carte_terre = carte_hauteur >= 0.3  # Zones de terre

# Définition des gradients de couleur en fonction de l'élévation
couleurs = [
    (0, 0, 0.5),  # Eau profonde
    (0, 0, 1),  # Eau peu profonde
    (0.8, 0.8, 0.2),  # Plage
    (0.2, 0.8, 0.2),  # Terre
    (0.3, 0.2, 0.1),  # Montagne (marron foncé)
    (1, 1, 1)  # Neige
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
            carte_couleur[i][j] = interpoler_couleur(carte_hauteur[i][j], [couleurs[0], couleurs[
                1]])  # Choix des couleurs d'eau profonde ou peu profonde
        else:  # Si c'est de la terre
            carte_couleur[i][j] = interpoler_couleur(carte_hauteur[i][j], [couleurs[3], couleurs[4], couleurs[
                5]])  # Choix des couleurs de terre, montagne ou neige

# Ajout des plages autour des zones d'eau
masque_eau_erode = np.pad(carte_eau, 1, mode='constant',
                          constant_values=True)  # Ajout d'une bordure d'eau pour éviter les problèmes de bords
masque_eau_erode = masque_eau_erode[:-2, :-2] | masque_eau_erode[1:-1, :-2] | masque_eau_erode[2:,
                                                                              :-2] | masque_eau_erode[:-2,
                                                                                     1:-1] | masque_eau_erode[2:,
                                                                                             1:-1] | masque_eau_erode[
                                                                                                     :-2,
                                                                                                     2:] | masque_eau_erode[
                                                                                                           1:-1,
                                                                                                           2:] | masque_eau_erode[
                                                                                                                 2:,
                                                                                                                 2:]  # Érosion de l'eau sur les bords
carte_plage = masque_eau_erode & carte_terre  # Intersection de l'eau érodée avec les zones de terre
carte_couleur[carte_plage] = interpoler_couleur(0.5, [couleurs[2], couleurs[3]])  # Coloration des plages

# Ajout de la neige sur les sommets des montagnes
carte_neige = carte_hauteur > 0.8  # Réglage du seuil pour les sommets de montagne
carte_couleur[carte_neige] = (1, 1, 1)  # Couleur de la neige

# Noms de villes vikings aléatoires
noms_villes_vikings = ["Asgard", "Valhalla", "Niflheim", "Midgard", "Jotunheim", "Helheim", "Svartalfheim", "Alfheim",
                       "Vanaheim", "Muspelheim", "Yggdrasil", "Ragnarok", "Bifrost", "Fenrir", "Nidavellir"]

# Génération de coordonnées et de noms de villes aléatoires
nb_villes = 10
coordonnees_villes = []
noms_villes = []

while len(coordonnees_villes) < nb_villes:
    x, y = np.random.randint(0, largeur), np.random.randint(0, hauteur)
    if carte_terre[x, y]:  # Vérification si la ville est sur la terre
        coordonnees_villes.append((x, y))
        noms_villes.append(random.choice(noms_villes_vikings))
        # Ajout d'un point marron clair sous la ville
        carte_couleur[x, y] = (0.8, 0.6, 0.4)

# Ajout des noms des villes sur la carte
for coordonnee_ville, nom_ville in zip(coordonnees_villes, noms_villes):
    # Ajustement des positions pour éviter les chevauchements
    dx, dy = 0, 0
    while any(np.linalg.norm(np.array(coordonnee_ville) - np.array(other)) < 10 for other in coordonnees_villes if
              other != coordonnee_ville):
        dx += random.randint(-20, 20)
        dy += random.randint(-20, 20)
        coordonnee_ville = (coordonnee_ville[0] + dx, coordonnee_ville[1] + dy)

    plt.text(coordonnee_ville[1], coordonnee_ville[0] - 5, nom_ville, color='black', fontsize=13, ha='center',
             va='center', fontfamily='cursive')

    # Ajout d'une icône de maison à côté de chaque ville
    plt.plot(coordonnee_ville[1], coordonnee_ville[0], marker='^', markersize=10, markerfacecolor='brown',
             markeredgewidth=1, markeredgecolor='black')

# Ajout de la légende en dehors de la carte
legende_elements = {
    'Eau profonde': 'blue',
    'Eau peu profonde': 'lightblue',
    'Plage': 'yellow',
    'Terre': 'green',
    'Montagne': 'brown',
    'Neige': 'white'
}
plt.legend(legende_elements.keys(), loc='upper left', bbox_to_anchor=(1, 1))

# Affichage de la carte de hauteur colorée en 2D avec zoom et déplacement activés
plt.imshow(carte_couleur, origin='lower')
plt.axis('off')  # Suppression des indications d'échelle sur les côtés
plt.title(None)  # Suppression du titre
mplcursors.cursor(hover=True)
plt.show()
