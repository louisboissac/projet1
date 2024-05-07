from flask import Flask, render_template, request
import generer_carte

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir la route pour la page d'accueil
@app.route('/')
def index():
    # Rendre le template HTML de la page d'accueil
    return render_template('index.html')

# Définir la route pour la page de génération de carte
@app.route('/generer_carte', methods=['POST'])
def generer_carte():
    # Récupérer les paramètres saisis par l'utilisateur
    largeur = int(request.form['largeur'])
    hauteur = int(request.form['hauteur'])
    echelle = float(request.form['echelle'])
    graine = int(request.form['graine'])
    niveau_eau = float(request.form['niveau_eau'])
    nb_villes = int(request.form['nb_villes'])

    # Générer la carte en utilisant le module "generer_carte"
    carte = generer_carte.generer_carte(largeur, hauteur, echelle, graine, niveau_eau, nb_villes)

    # Récupérer les données de la carte depuis la base de données
    conn = psycopg2.connect(
        dbname="MapBase",
        user="Carte_fictif",
        password="Mapcarte",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM carte")
    données_carte = cur.fetchall()
    cur.close()
    conn.close()

    # Rendre le template HTML de la page de génération de carte avec les données de la carte
    return render_template('carte.html', données_carte=données_carte)

# Exécuter l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
