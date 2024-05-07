# Connectez-vous à la base de données
conn = psycopg2.connect(
    dbname="MapBase",
    user="Carte_fictif",
    password="Mapcarte",
    host="localhost"
)

# Créez un curseur pour exécuter des requêtes SQL
cur = conn.cursor()

# Insérez les données de la carte dans le tableau
for i in range(largeur):
    for j in range(hauteur):
        hauteur_case = carte_hauteur[i][j]
        type_terrain_case = "eau" if carte_eau[i][j] else "terre" if carte_terre[i][j] else "plage" if carte_plage[i][j] else "montagne" if carte_hauteur[i][j] > 0.5 else "neige" if carte_hauteur[i][j] > 0.8 else "terre"
        nom_ville_case = None
        if (i, j) in coordonnees_villes_esp:
            nom_ville_case = noms_villes[coordonnees_villes_esp.index((i, j))]
        nom_site_historique_case = None
        if (i, j) in sites_historiques.values():
            nom_site_historique_case = list(sites_historiques.keys())[list(sites_historiques.values()).index((i, j))]
        cur.execute("""
            INSERT INTO carte (x, y, hauteur, type_terrain, nom_ville, nom_site_historique)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (i, j, hauteur_case, type_terrain_case, nom_ville_case, nom_site_historique_case))

# Validez l'insertion des données
conn.commit()

# Fermez le curseur et la connexion à la base de données
cur.close()
conn.close()
