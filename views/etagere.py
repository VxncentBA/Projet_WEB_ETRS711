from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)

from models.etagere import Etagere
from models.cave import Cave

etagere_routes = Blueprint("etagere", __name__)

@etagere_routes.route("/creer_etagere", methods=["GET", "POST"])
def creer_etagere():
    if "logged_in" in session and session["logged_in"]:
        if request.method == "POST":
            region = request.form["region"]
            capacite = request.form["capacite"]
            numero=request.form["numero"],
            cave_id = request.form["cave_id"]
            print(region, capacite, numero, cave_id)

            # Obtenez le nouvel ID de l'etagere en utilisant la méthode obtenir_dernier_id_etagere
            dernier_id_etagere = Etagere.obtenir_dernier_id_etagere()
            nouvel_id_etagere = dernier_id_etagere + 1

            nouvelle_etagere = Etagere(
                id_etagere=int(nouvel_id_etagere),
                numero=int(numero[0]),
                region=region,
                capacite=int(capacite),
                cave_associee=Cave(cave_id, None, None),
            )
            nouvelle_etagere.INSERT()

            flash("Nouvelle etagere créée avec succès!", "success")
            return redirect(url_for("accueil"))
        else:
            caves = Cave.get_utilisateur_caves(session.get("user_id")) # Récupérer les caves de l'utilisateur connecté
            output = []
            for cave in caves:
                output.append({"id_cave": cave.id_cave, "nom_cave": cave.nom_cave})
            return render_template("creer_etagere.html", caves=output)
    else:
        flash("Vous devez être connecté pour créer une etagere.", "error")
        return redirect(url_for("users.login"))
