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

    # Affichez le formulaire de saisie des données de la carte
    return render_template('interface2.html', carte_image=carte_image)

if __name__ == '__main__':
    initialiser_base_donnees()
    app.run(debug=True)
