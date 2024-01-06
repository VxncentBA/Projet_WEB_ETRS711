from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)

from models.bouteille import Bouteille
from models.etagere import Etagere

bouteille_routes = Blueprint("bouteille", __name__)

@bouteille_routes.route("/ajouter_bouteille", methods=["GET", "POST"])

def ajouter_bouteille():
    if "logged_in" in session and session["logged_in"]:
        if request.method == "POST":
            domaine_viticole = request.form["domaine_viticole"]
            nom = request.form["nom"]
            type = request.form["type"]
            annee = request.form["annee"]
            region = request.form["region"]
            commentaires = request.form.get("commentaires", "")
            note_personnelle = request.form["note_personnelle"]
            note_moyenne = request.form.get("note_moyenne", "")
            photo_etiquette = request.form["photo_etiquette"]
            prix = request.form["prix"]

           
            # Obtenez le nouvel ID de la bouteille en utilisant la méthode obtenir_dernier_id_bouteille
            dernier_id_bouteille = Bouteille.obtenir_dernier_id_bouteille()
            nouvel_id_bouteille = dernier_id_bouteille + 1

            nouvelle_bouteille = Bouteille(
                id_bouteille=nouvel_id_bouteille,
                domaine_viticole=domaine_viticole,
                nom=nom,
                type=type,
                annee=annee,
                region=region,
                commentaires=commentaires,
                note_personnelle=note_personnelle,
                note_moyenne=note_moyenne,
                photo_etiquette=photo_etiquette,
                prix=prix,
            )
            nouvelle_bouteille.INSERT()

            flash("Nouvelle bouteille créée avec succès!", "success")
            return redirect(url_for("accueil"))
        else:
            return render_template("ajouter_bouteille.html")
    else:
        flash("Vous devez être connecté pour ajouter une bouteille.", "error")
        return redirect(url_for("users.login"))

@ajouter_bouteille_cave.route("/ajouter_bouteille_cave", methods=["GET", "POST"])

def ajouter_bouteille_cave():
    if "logged_in" in session and session["logged_in"]: