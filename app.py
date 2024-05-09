from flask import Flask, render_template, request
from carte_avc_modif import generate_map

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        taille_carte = int(request.form['taille_carte'])
        niv_eau = float(request.form['niv_eau'])
        niv_montagne = float(request.form['niv_montagne'])
        niv_plaine = float(request.form['niv_plaine'])
        niv_foret = float(request.form['niv_foret'])
        nombre_villes = int(request.form['nombre_villes'])

        carte_image = generate_map(taille_carte, niv_eau, niv_montagne, niv_plaine, niv_foret, nombre_villes)

        return render_template('interface2.html', carte_image=carte_image)
    else:
        return render_template('interface2.html')

if __name__ == '__main__':
    app.run(debug=True)






