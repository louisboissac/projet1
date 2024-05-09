from flask import Flask, render_template, request
# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir la route pour la page d'accueil
@app.route('/')
def index():
    # Rendre le template HTML de la page d'accueil
    return render_template('interface.html')


# Exécuter l'application Flask
if __name__ == '__main__':
    app.run(debug=True)




