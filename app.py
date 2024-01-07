import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
)
from models.cave import Cave

# Import route in a separate file
from views.utilisateur import utilisateur_routes
from views.cave import cave_routes
from views.etagere import etagere_routes
from views.bouteille import bouteille_routes

# Create Instance of Flask Server
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "test"

# Add other file route, to our app
app.register_blueprint(utilisateur_routes)
app.register_blueprint(cave_routes)
app.register_blueprint(etagere_routes)
app.register_blueprint(bouteille_routes)


# Home route
@app.route("/")
@app.route("/accueil")
def accueil():
    if "logged_in" in session and session["logged_in"]:
        nom_utilisateur = session["username"]

        caves_utilisateur = Cave.afficher_details_cave(session["user_id"])

        if request.args.get("response") == "json":
            return jsonify({"status": "success", "msg": caves_utilisateur}), 200
        else:
            print(caves_utilisateur)
            for cave in caves_utilisateur:
                print(cave.to_dict())
            return render_template(
                "accueil.html",
                nom_utilisateur=nom_utilisateur,
                caves_utilisateur=caves_utilisateur,
            )
    else:
        return redirect(url_for("users.deconnexion"))  # Rediriger vers la page de connexion après la déconnexion



# Debug route
@app.route("/debug")
def afficher_tables():
    conn = sqlite3.connect("bdd.db")
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

    return render_template(
        "affichage_tables.html",
        utilisateurs=utilisateurs,
        caves=caves,
        etageres=etageres,
        bouteilles=bouteilles,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
