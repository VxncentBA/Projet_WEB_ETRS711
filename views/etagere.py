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
from models.bouteille import Bouteille

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

@etagere_routes.route("/etagere/<int:id_etagere>/ajouter", methods=["GET", "POST"])

def ajouter_bouteille_etagere(id_etagere):
    if "logged_in" in session and session["logged_in"]:
        if request.method == "POST":
            bouteille_id = request.form["bouteille_id"]
            etagere_id = id_etagere
            
            if Etagere.get_emplacement_disponibles(id_etagere) > 0:

                Etagere.ajouter_bouteille_etagere(etagere_id, bouteille_id)
                flash("Nouvelle bouteille créée avec succès!", "success")

            
            return redirect(url_for("accueil"))
        else:
            bouteilles = Bouteille.get_bouteilles()
            output = []
            for bouteille in bouteilles:
                output.append({"id_bouteille": bouteille.id_bouteille, "nom_bouteille": bouteille.nom})
            return render_template("ajouter_bouteille_etagere.html", bouteilles=output, etagere_id=id_etagere)
    else:
        flash("Vous devez être connecté pour ajouter une bouteille.", "error")
        return redirect(url_for("users.login"))


@etagere_routes.route("/supprimer_etagere/<int:id_etagere>", methods=["GET", "POST"])

def supprimer_etagere(id_etagere):
    if "logged_in" in session and session["logged_in"]:
        etagere = Etagere(id_etagere, None, None, None, None)
        etagere.DELETE()
        flash("Etagere supprimée avec succès!", "success")
        return redirect(url_for("accueil"))
    else:
        flash("Vous devez être connecté pour supprimer une etagere.", "error")
        return redirect(url_for("users.login"))


@etagere_routes.route("/etagere/<int:id_etagere>/supprimer", methods=["GET", "POST"])

def supprimer_bouteille_etagere(id_etagere):
    if "logged_in" in session and session["logged_in"]:
        if request.method == "POST":
            bouteille_id = request.form["bouteille_id"]
            etagere_id = id_etagere
            
            Etagere.supprimer_bouteille_etagere(etagere_id, bouteille_id)
            flash("Bouteille supprimée avec succès!", "success")

            return redirect(url_for("accueil"))
        else:
            bouteilles = Bouteille.get_bouteilles()
            output = []
            for bouteille in bouteilles:
                output.append({"id_bouteille": bouteille.id_bouteille, "nom_bouteille": bouteille.nom})
            return render_template("supprimer_bouteille_etagere.html", bouteilles=output, etagere_id=id_etagere)
    else:
        flash("Vous devez être connecté pour supprimer une bouteille.", "error")
        return redirect(url_for("users.login"))