import sqlite3
from Vin_de_Vincent import *
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def accueil():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Utilisateurs")
    utilisateurs = c.fetchall()
    conn.close()
    return render_template('accueil.html', utilisateurs=utilisateurs)

@app.route('/tables')
def afficher_tables():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()

    # Récupération des données de la table Utilisateurs
    c.execute("SELECT * FROM Utilisateurs")
    utilisateurs = c.fetchall()

    # Récupération des données de la table Caves
    c.execute("SELECT * FROM Caves")
    caves = c.fetchall()

    # Récupération des données de la table Etageres
    c.execute("SELECT * FROM Etageres")
    etageres = c.fetchall()

    # Récupération des données de la table Bouteilles associées à chaque étagère
    c.execute("SELECT * FROM Bouteilles")
    bouteilles = c.fetchall()
    # c.execute("""
    # SELECT Bouteilles.*
    # FROM Bouteilles
    # JOIN EtagereBouteille ON Bouteilles.id_bouteille = EtagereBouteille.id_bouteille
    # JOIN Etageres ON Etageres.id_etagere = EtagereBouteille.id_etagere
    # """)
    # bouteilles = c.fetchall()
    conn.close()

    return render_template('affichage_tables.html', utilisateurs=utilisateurs, caves=caves, etageres=etageres, bouteilles=bouteilles) #

@app.route('/creer_utilisateur', methods=['GET', 'POST'])
def creer_utilisateur():
    if request.method == 'POST':
        id_utilisateur = request.form['id_utilisateur']
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        email = request.form['email']

        nouvel_utilisateur = Utilisateur(
            id_utilisateur=id_utilisateur,
            nom_utilisateur=nom_utilisateur,
            mot_de_passe=mot_de_passe,
            email=email
        )

        nouvel_utilisateur.sauvegarder_dans_bdd()
        
        return "Nouvel utilisateur créé avec succès"
    else:
        return render_template('creer_utilisateur.html')


if __name__ == '__main__':
    app.run(debug=True)