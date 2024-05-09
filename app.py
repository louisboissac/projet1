from flask import Flask, render_template,request
from carte_avc_modif import generate_map





# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir la route pour la page d'accueil
def index():
    if request.method == 'POST':
        # Récupérer les valeurs des paramètres depuis le formulaire
        taille_carte = int(request.form['taille_carte'])
        niv_eau = float(request.form['niv_eau'])
        niv_montagne = float(request.form['niv_montagne'])
        niv_plaine = float(request.form['niv_plaine'])
        niv_foret = float(request.form['niv_foret'])
        nombre_villes = int(request.form['nombre_villes'])

        # Générer la carte avec les paramètres choisis par l'utilisateur
        carte_image = generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)

        # Rendre le template HTML de la page d'accueil avec l'image de la carte
        return render_template('interface.html', carte_image=carte_image)
    else:
        # Si c'est une requête GET, simplement afficher le formulaire
        return render_template('interface.html')

# Exécuter l'application Flask
if __name__ == '__main__':
    app.run(debug=True)




