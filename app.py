from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from carte_avc_modif import generate_map

app = Flask(__name__)

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
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    carte_image = None
    if request.method == 'POST':
        if 'regenerer' in request.form or 'generer' in request.form:
            # Récupérez les données du formulaire
            taille_carte = int(request.form.get('taille_carte'))
            niv_eau = float(request.form.get('niv_eau'))
            niv_montagne = float(request.form.get('niv_montagne'))
            niv_plaine = float(request.form.get('niv_plaine'))
            niv_foret = float(request.form.get('niv_foret'))
            nombre_villes = int(request.form.get('nombre_villes'))

            # Générez la carte
            carte_image = generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)
        elif 'sauvegarder' in request.form:
            # Récupérez les données du formulaire
            taille_carte = int(request.form.get('taille_carte'))
            niv_eau = float(request.form.get('niv_eau'))
            niv_montagne = float(request.form.get('niv_montagne'))
            niv_plaine = float(request.form.get('niv_plaine'))
            niv_foret = float(request.form.get('niv_foret'))
            nombre_villes = int(request.form.get('nombre_villes'))

            # Enregistrez les informations dans la base de données
            conn = sqlite3.connect('vikings_map.db')
            c = conn.cursor()
            c.execute('''
            INSERT INTO map_info (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes))
            conn.commit()
            conn.close()

            # Générez la carte
            carte_image = generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)

    # Affichez le formulaire de saisie des données de la carte
    return render_template('interface2.html', carte_image=carte_image)

@app.route('/sauvegarder', methods=['POST'])
def sauvegarder_carte():
    if request.method == 'POST':
        # Récupérez les données du formulaire
        taille_carte = int(request.form.get('taille_carte'))
        niv_eau = float(request.form.get('niv_eau'))
        niv_montagne = float(request.form.get('niv_montagne'))
        niv_plaine = float(request.form.get('niv_plaine'))
        niv_foret = float(request.form.get('niv_foret'))
        nombre_villes = int(request.form.get('nombre_villes'))

        # Afficher les données récupérées du formulaire
        print("Données du formulaire :")
        print("Taille de la carte :", taille_carte)
        print("Niveau d'eau :", niv_eau)
        print("Niveau de montagne :", niv_montagne)
        print("Niveau de plaine :", niv_plaine)
        print("Niveau de forêt :", niv_foret)
        print("Nombre de villes :", nombre_villes)

        # Enregistrez les informations dans la base de données
        conn = sqlite3.connect('vikings_map.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO map_info (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes))
        conn.commit()
        conn.close()

        # Générez la carte
        carte_image = generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)

        # Redirigez l'utilisateur vers la page d'accueil
        return render_template('interface2.html', carte_image=carte_image)

    # Si la méthode de requête n'est pas POST, redirigez l'utilisateur vers la page d'accueil
    return redirect(url_for('index'))


@app.route('/cartes-sauvegardees')
def cartes_sauvegardees():
    # Récupérez les cartes sauvegardées depuis la base de données
    conn = sqlite3.connect('vikings_map.db')
    c = conn.cursor()
    c.execute('SELECT * FROM map_info')
    cartes_sauvegardees = c.fetchall()
    conn.close()

    # Affichez la page des cartes sauvegardées avec les données récupérées
    return render_template('cartes_sauvegardees.html', cartes_sauvegardees=cartes_sauvegardees)

@app.route('/voir-carte/<int:carte_id>')
def voir_carte(carte_id):
    # Récupérez les informations de la carte depuis la base de données en utilisant son ID
    conn = sqlite3.connect('vikings_map.db')
    c = conn.cursor()
    c.execute('SELECT * FROM map_info WHERE id = ?', (carte_id,))
    carte = c.fetchone()
    conn.close()

    # Affichez les détails de la carte dans un template HTML dédié
    return render_template('detail_carte.html', carte=carte)


if __name__ == '__main__':
    initialiser_base_donnees()
    app.run(debug=True)
