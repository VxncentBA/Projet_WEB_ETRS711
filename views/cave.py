from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from models.cave import Cave
from models.utilisateur import Utilisateur

cave_routes = Blueprint("caves", __name__)


@cave_routes.route("/creer_cave", methods=["GET", "POST"])
def creer_cave():
    if "logged_in" in session and session["logged_in"]:
        if request.method == "POST":
            nom_cave = request.form["nom_cave"]
            user_id = session["user_id"]

            # Obtenez le nouvel ID de la cave en utilisant la méthode obtenir_dernier_id_cave
            dernier_id_cave = Cave.obtenir_dernier_id_cave()
            nouvel_id_cave = dernier_id_cave + 1

            nouvelle_cave = Cave(
                id_cave=nouvel_id_cave,
                nom_cave=nom_cave,
                proprietaire=Utilisateur(user_id, None, None, None),
            )
            nouvelle_cave.INSERT()

            flash("Nouvelle cave créée avec succès!", "success")
            return redirect(url_for("accueil"))
        else:
            return render_template("creer_cave.html")
    else:
        flash("Vous devez être connecté pour créer une cave.", "error")
        return redirect(url_for("users.login"))

@cave_routes.route("/supprimer_cave/<int:id_cave>", methods=["GET", "POST"])
def supprimer_cave(id_cave):
    if "logged_in" in session and session["logged_in"]:
        cave = Cave(id_cave, None, None)
        cave.DELETE()
        flash("Cave supprimée avec succès!", "success")
        return redirect(url_for("accueil"))
    else:
        flash("Vous devez être connecté pour supprimer une cave.", "error")
        return redirect(url_for("users.login"))