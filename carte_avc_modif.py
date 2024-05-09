import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random

def generate_map(taille_carte,niv_eau,niv_montagne,niv_plaine,niv_foret,nombre_villes,):
    # Définition de la taille de la carte en hauteur et en largeur
    largeur = taille_carte
    hauteur = taille_carte

    # Définition de l'échelle du bruit (affecte le niveau de détail)
    echelle = taille_carte/2

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

    # Génération d'une carte pour les zones d'eau, de plaines, de forêts et de montagnes
    carte_eau = np.zeros((largeur, hauteur))  # Initialisation de la carte d'eau
    seuil_eau = niv_eau  # Réglage du seuil pour les zones d'eau
    carte_eau[carte_hauteur < seuil_eau] = 1  # Marquage des zones d'eau

    carte_plaine = np.zeros((largeur, hauteur))  # Initialisation de la carte de plaines
    seuil_plaine = niv_plaine  # Réglage du seuil pour les zones de plaines
    carte_plaine[(carte_hauteur >= seuil_eau) & (carte_hauteur < seuil_plaine)] = 1  # Marquage des zones de plaines

    carte_foret = np.zeros((largeur, hauteur))  # Initialisation de la carte de forêts
    seuil_foret = niv_foret  # Réglage du seuil pour les zones de forêt
    carte_foret[(carte_hauteur >= seuil_plaine) & (carte_hauteur < seuil_foret)] = 1  # Marquage des zones de forêts

    carte_montagne = np.zeros((largeur, hauteur))  # Initialisation de la carte de montagnes
    seuil_montagne = niv_montagne  # Réglage du seuil pour les zones de montagne
    carte_montagne[carte_hauteur >= seuil_foret] = 1  # Marquage des zones de montagnes

    # Définition des gradients de couleur en fonction de l'élévation
    couleurs = [
        (0, 0, 0.5),  # Eau profonde
        (0, 0, 1),  # Eau peu profonde
        (0.8, 0.8, 0.2),  # Plage
        (0.2, 0.8, 0.2),  # Plaine (vert clair)
        (0, 0.5, 0),  # Forêt (vert foncé)
        (0.3, 0.2, 0.1),  # Montagne (marron foncé)
        (1, 1, 1)  # Neige (blanc)
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
            elif carte_plaine[i][j]:  # Si c'est une plaine
                carte_couleur[i][j] = couleurs[3]  # Vert clair pour les plaines
            elif carte_foret[i][j]:  # Si c'est une forêt
                carte_couleur[i][j] = couleurs[4]  # Vert foncé pour les forêts
            elif carte_montagne[i][j]:  # Si c'est une montagne
                carte_couleur[i][j] = couleurs[5]  # Marron foncé pour les montagnes
                if carte_hauteur[i][j] > 0.85:  # Ajoutez de la neige pour les zones de montagnes élevées
                    carte_couleur[i][j] = couleurs[6]  # Neige

    # Ajout des plages autour des zones d'eau
    masque_eau_erode = np.pad(carte_eau.astype(int), 1, mode='constant', constant_values=1)
    masque_eau_erode = masque_eau_erode[:-2, :-2] + masque_eau_erode[1:-1, :-2] + masque_eau_erode[2:, :-2] + \
                        masque_eau_erode[:-2, 1:-1] + masque_eau_erode[2:, 1:-1] + masque_eau_erode[:-2, 2:] + \
                        masque_eau_erode[1:-1, 2:] + masque_eau_erode[2:, 2:]
    masque_eau_erode = (masque_eau_erode > 0).astype(int)  # Convertir en tableau booléen
    carte_plage = (masque_eau_erode * carte_plaine) > 0
    carte_couleur[carte_plage] = interpoler_couleur(0.5, [couleurs[2], couleurs[3]])


    # Définition des noms de villes vikings aléatoires
    noms_villes_vikings = ["Asgard", "Valhalla", "Niflheim", "Midgard", "Jotunheim", "Helheim", "Svartalfheim",
                           "Alfheim", "Vanaheim", "Muspelheim", "Yggdrasil", "Ragnarok", "Bifrost", "Fenrir",
                           "Nidavellir"]

    # Génération de coordonnées et de noms de villes aléatoires
    nb_villes = nombre_villes
    coordonnees_villes_esp = set()  # Utilisation d'un ensemble pour stocker les coordonnées espacées des villes
    noms_villes = []

    def check_overlap(pos1, pos2, text_width=10, text_height=5):
        """Vérifie si deux éléments se superposent."""
        x1, y1 = pos1
        x2, y2 = pos2
        return not (x1 + text_width < x2 or x2 + text_width < x1 or y1 + text_height < y2 or y2 + text_height < y1)

    while len(coordonnees_villes_esp) < nb_villes:
        x, y = np.random.randint(10, largeur - 10), np.random.randint(10,
                                                                      hauteur - 10)  # Assure que les villes ne se situent pas trop près des bords de la carte
        if 10 <= x < largeur - 10 and 10 <= y < hauteur - 10:  # Vérification si les coordonnées sont à l'intérieur de la carte
            if carte_plaine[x, y] and not carte_eau[
                x, y]:  # Vérification si la ville est sur une plaine et n'est pas dans l'eau
                # Vérification des zones d'exclusion autour de la ville
                exclusion_zone = set((x + i, y + j) for i in range(-15, 16) for j in range(-15, 16))
                if not coordonnees_villes_esp.intersection(
                        exclusion_zone):  # Si aucune intersection avec les villes déjà placées
                    coordonnees_villes_esp.add((x, y))
                    nom_ville = random.choice(noms_villes_vikings)
                    noms_villes_vikings.remove(
                        nom_ville)  # Supprimer le nom de ville utilisé pour éviter les répétitions
                    noms_villes.append((nom_ville, (x, y)))

    # Sites historiques
    sites_historiques = {
        "Ruines de Valhalla": None,
        "Bataille de Ragnarok": None,
        "Tombe de Yggdrasil": None,
        "Autel de Thor": None,
        "Grotte de Fenrir": None,
    }

    # Attribution des coordonnées aléatoires aux sites historiques sans chevauchement
    for nom_site in sites_historiques:
        x, y = np.random.randint(20, largeur - 20), np.random.randint(20, hauteur - 20)
        while not carte_plaine[x, y] or any(
                np.linalg.norm(np.array((x, y)) - np.array(site)) < 30 for site in coordonnees_villes_esp) or any(
                site is not None and np.linalg.norm(np.array((x, y)) - np.array(site)) < 30 for site in
                sites_historiques.values()):
            x, y = np.random.randint(20, largeur - 20), np.random.randint(20, hauteur - 20)
        sites_historiques[nom_site] = (x, y)

    # Ajustement des positions pour éviter le chevauchement des noms de villes et de sites historiques
    for i in range(len(noms_villes)):
        name1, pos1 = noms_villes[i]
        for j in range(i + 1, len(noms_villes)):
            name2, pos2 = noms_villes[j]
            if check_overlap(pos1, pos2):
                noms_villes[j] = (name2, (pos2[0], pos2[1] + 5))

    for nom_site1, pos_site1 in sites_historiques.items():
        for nom_site2, pos_site2 in sites_historiques.items():
            if nom_site1 != nom_site2 and check_overlap(pos_site1, pos_site2):
                x, y = pos_site2
                sites_historiques[nom_site2] = (x, y + 5)

    # Génération de la carte avec les sites historiques
    for nom_site, coordonnee_site in sites_historiques.items():
        x, y = coordonnee_site
        carte_couleur[x, y] = (1, 0, 0)  # Couleur des sites historiques

    # Affichage de la carte de hauteur colorée en 2D avec zoom et déplacement activés
    fig, ax = plt.subplots(figsize=(8, 6))  # Définition de la taille de la figure
    im = ax.imshow(carte_couleur, origin='lower')
    ax.axis('off')  # Suppression des indications d'échelle sur les côtés

    # Ajout des points noirs pour marquer les emplacements des villes
    for nom_ville, coordonnee_ville in noms_villes:
        x, y = coordonnee_ville
        if 0 <= x < largeur and 0 <= y < hauteur:  # Vérification que les coordonnées de la ville sont dans les limites de la carte
            ax.plot(y, x, marker='o', markersize=5, color='black')  # Ajout du point noir pour marquer la ville
            ax.text(y, x + 7, nom_ville, color='black', fontsize=10, ha='center', va='center',
                    fontfamily='cursive')  # Ajout du nom de la ville au-dessus du point avec la police cursive

    # Ajout des points rouges pour marquer les emplacements des sites historiques
    for nom_site, coordonnee_site in sites_historiques.items():
        x, y = coordonnee_site
        if 0 <= x < largeur and 0 <= y < hauteur:  # Vérification que les coordonnées du site historique sont dans les limites de la carte
            ax.plot(y, x, marker='o', markersize=5,
                    color='red')  # Ajout du point rouge pour marquer le site historique avec une taille de point plus grande
            ax.text(y, x + 7, nom_site, color='red', fontsize=8, ha='center', va='center',
                    fontfamily='cursive')  # Ajout du nom du site historique au-dessus du point avec la police cursive

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
    pass










