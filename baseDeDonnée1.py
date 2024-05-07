import psycopg2

# Connectez-vous à la base de données
conn = psycopg2.connect(
    dbname="MapBase",
    user="Carte_fictif",
    password="Mapcarte",
    host="localhost"
)

# Créez un curseur pour exécuter des requêtes SQL
cur = conn.cursor()

# Créez un tableau pour stocker les données de la carte
cur.execute("""
    CREATE TABLE carte (
        id SERIAL PRIMARY KEY,
        x INTEGER,
        y INTEGER,
        hauteur REAL,
        type_terrain VARCHAR(20),
        nom_ville VARCHAR(50),
        nom_site_historique VARCHAR(50)
    )
""")

# Validez la création du tableau
conn.commit()

# Fermez le curseur et la connexion à la base de données
cur.close()
conn.close()
