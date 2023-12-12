import sqlite3, bcrypt
from Vin_de_Vincent import *
from flask import Flask, render_template, request, session, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'vincent'

# Cette fonction vérifie le mot de passe haché avec bcrypt
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

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

        if Utilisateur.utilisateur_existe(id_utilisateur):
            return "Utilisateur avec cet ID existe déjà"
        else:
            hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
            nouvel_utilisateur = Utilisateur(
                id_utilisateur=id_utilisateur,
                nom_utilisateur=nom_utilisateur,
                mot_de_passe=hashed_password,
                email=email
            )
            nouvel_utilisateur.sauvegarder_dans_bdd()
            return "Nouvel utilisateur créé avec succès"
    else:
        return render_template('creer_utilisateur.html')

@app.route('/supprimer_utilisateur', methods=['GET', 'POST'])
def supprimer_utilisateur():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()
    c.execute("SELECT id_utilisateur, nom_utilisateur FROM Utilisateurs")
    utilisateurs = c.fetchall()
    conn.close()

    if request.method == 'POST':
        id_utilisateur_a_supprimer = request.form['utilisateur']
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()

        c.execute("DELETE FROM Etageres WHERE cave_associee_id IN (SELECT id_cave FROM Caves WHERE proprietaire_id = ?)",
                  (id_utilisateur_a_supprimer,))
        c.execute("DELETE FROM Bouteilles WHERE id_bouteille IN (SELECT id_bouteille FROM Etageres WHERE cave_associee_id IN (SELECT id_cave FROM Caves WHERE proprietaire_id = ?))",
                  (id_utilisateur_a_supprimer,))
        c.execute("DELETE FROM Caves WHERE proprietaire_id = ?", (id_utilisateur_a_supprimer,))
        c.execute("DELETE FROM Utilisateurs WHERE id_utilisateur = ?", (id_utilisateur_a_supprimer,))

        conn.commit()
        conn.close()
        return "Utilisateur supprimé avec ses éléments associés"

    return render_template('supprimer_utilisateur.html', utilisateurs=utilisateurs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        # Recherche de l'utilisateur dans la base de données
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("SELECT id_utilisateur, nom_utilisateur, mot_de_passe FROM Utilisateurs WHERE nom_utilisateur = ?", (nom_utilisateur,))
        utilisateur = c.fetchone()
        conn.close()

        if utilisateur and verify_password(utilisateur[2], mot_de_passe):
            # L'utilisateur est authentifié, stocker l'ID de l'utilisateur dans la session
            session['logged_in'] = True
            session['user_id'] = utilisateur[0]  # Stocker l'ID de l'utilisateur dans la session
            session['username'] = nom_utilisateur  # Stocker le nom d'utilisateur dans la session
            flash('Connecté avec succès!', 'success')
            return redirect(url_for('accueil'))
        else:
            # Afficher un message d'erreur en cas d'échec d'authentification
            flash('Identifiants incorrects. Veuillez réessayer.', 'error')

    return render_template('login.html')


@app.route('/deconnexion')
def deconnexion():
    session.pop('logged_in', None)  # Supprimer la clé 'logged_in' de la session
    session.pop('username', None)   # Supprimer le nom d'utilisateur de la session
    return redirect(url_for('login'))  # Rediriger vers la page de connexion

@app.route('/creer_cave', methods=['GET', 'POST'])
def creer_cave():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            nom_cave = request.form['nom_cave']
            user_id = session['user_id']

            # Obtenez le nouvel ID de la cave en utilisant la méthode obtenir_dernier_id_cave
            dernier_id_cave = Cave.obtenir_dernier_id_cave()
            nouvel_id_cave = dernier_id_cave + 1

            nouvelle_cave = Cave(id_cave=nouvel_id_cave, nom_cave=nom_cave, proprietaire=Utilisateur(user_id, None, None, None))
            nouvelle_cave.sauvegarder_dans_bdd()

            flash('Nouvelle cave créée avec succès!', 'success')
            return redirect(url_for('accueil'))
        else:
            return render_template('creer_cave.html')
    else:
        flash('Vous devez être connecté pour créer une cave.', 'error')
        return redirect(url_for('login'))


@app.route('/accueil')
def accueil():
    if 'logged_in' in session and session['logged_in']:
        nom_utilisateur = session['username']
        
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        
        # Récupérer les caves de l'utilisateur connecté
        caves_utilisateur = Cave.recuperer_caves_utilisateur(session['user_id'])

        # Récupérer les étagères pour chaque cave de l'utilisateur
        for cave in caves_utilisateur:
            c.execute("SELECT * FROM Etageres WHERE cave_associee_id = ?", (cave.id_cave,))
            etageres_cave = c.fetchall()
            cave.etageres = [Etagere(row[0], row[1], row[2], row[3], cave) for row in etageres_cave]

        conn.close()

        return render_template('accueil.html', nom_utilisateur=nom_utilisateur, caves_utilisateur=caves_utilisateur)
    else:
        return redirect(url_for('login'))


@app.route('/ajouter_bouteille/<int:id_cave>', methods=['POST'])
def ajouter_bouteille(id_cave):
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            nom_bouteille = request.form['nom_bouteille']
            
            # Vérifie si la cave appartient à l'utilisateur connecté
            cave = Cave.recuperer_cave_par_id(id_cave)
            if cave and cave.proprietaire.id_utilisateur == session['user_id']:
                # Création de la bouteille
                # ... (implémentez la création de la bouteille)

                # Ajout de la bouteille à la cave
                cave.ajouter_bouteille(nouvelle_bouteille)
                
                flash('Bouteille ajoutée à la cave avec succès!', 'success')
                return redirect(url_for('accueil'))
            else:
                flash('Cette cave n\'appartient pas à cet utilisateur.', 'error')
                return redirect(url_for('accueil'))
    else:
        flash('Vous devez être connecté pour ajouter une bouteille.', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)