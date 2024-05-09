import sqlite3

# Créez une connexion à la base de données SQLite
conn = sqlite3.connect('vikings_map.db')

# Créez un curseur pour exécuter des commandes SQL
c = conn.cursor()
# Créez la table pour stocker les informations de la carte
c.execute('''
CREATE TABLE IF NOT EXISTS map_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    taille_carte INTEGER,
    niv_eau REAL,
    niv_montagne REAL,
    niv_plaine REAL,
    niv_foret REAL,
    nombre_villes INTEGER
)
''')

# Créez la table pour stocker les informations des villes
c.execute('''
CREATE TABLE IF NOT EXISTS villes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_ville TEXT,
    x INTEGER,
    y INTEGER,
    map_info_id INTEGER,
    FOREIGN KEY (map_info_id) REFERENCES map_info (id)
)
''')

# Créez la table pour stocker les informations des sites historiques
c.execute('''
CREATE TABLE IF NOT EXISTS sites_historiques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_site TEXT,
    x INTEGER,
    y INTEGER,
    map_info_id INTEGER,
    FOREIGN KEY (map_info_id) REFERENCES map_info (id)
)
''')

# Enregistrez les modifications dans la base de données
conn.commit()
def generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes):
    # ... (le reste du code de la fonction generate_map) ...

    # Enregistrez les informations de la carte dans la base de données
    c.execute('''
    INSERT INTO map_info (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes))

    map_info_id = c.lastrowid

    # Enregistrez les informations des villes dans la base de données
    for nom_ville, coordonnee_ville in noms_villes:
        x, y = coordonnee_ville
        c.execute('''
        INSERT INTO villes (nom_ville, x, y, map_info_id)
        VALUES (?, ?, ?, ?)
        ''', (nom_ville, x, y, map_info_id))

    # Enregistrez les informations des sites historiques dans la base de données
    for nom_site, coordonnee_site in sites_historiques.items():
        x, y = coordonnee_site
        c.execute('''
        INSERT INTO sites_historiques (nom_site, x, y, map_info_id)
        VALUES (?, ?, ?, ?)
        ''', (nom_site, x, y, map_info_id))

    # Enregistrez les modifications dans la base de données
    conn.commit()

    # ... (le reste du code de la fonction generate_map) ...
# Fermez la connexion à la base de données
conn.close()
