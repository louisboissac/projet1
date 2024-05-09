import sqlite3

def initialiser_base_donnees():
    # Créez une connexion à la base de données SQLite
    conn = sqlite3.connect('vikings_map.db')
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
    conn.commit()
    conn.close()

def inserer_donnees_carte(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes):
    # Créez une connexion à la base de données SQLite
    conn = sqlite3.connect('vikings_map.db')
    c = conn.cursor()
    # Enregistrez les informations de la carte dans la base de données
    c.execute('''
    INSERT INTO map_info (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes))
    conn.commit()
    conn.close()
