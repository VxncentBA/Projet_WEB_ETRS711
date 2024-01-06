from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from models.utilisateur import Utilisateur
import bcrypt

utilisateur_routes = Blueprint("users", __name__)


# Cette fonction vérifie le mot de passe haché avec bcrypt
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password)


@utilisateur_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        nom_utilisateur = request.form["nom_utilisateur"]
        mot_de_passe = request.form["mot_de_passe"]

        utilisateur = Utilisateur.get_user_by_username(nom_utilisateur)
        print(utilisateur)

        if utilisateur and verify_password(utilisateur[2], mot_de_passe):
            session["logged_in"] = True
            session["user_id"] = utilisateur[
                0
            ]  # Stocker l'ID de l'utilisateur dans la session
            session[
                "username"
            ] = nom_utilisateur  # Stocker le nom d'utilisateur dans la session

            flash("Connecté avec succès!", "success")
            return redirect(url_for("accueil"))
        else:
            # Afficher un message d'erreur en cas d'échec d'authentification
            flash("Identifiants incorrects. Veuillez réessayer.", "error")


@utilisateur_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")
    else:
        id_utilisateur = request.form["id_utilisateur"]
        nom_utilisateur = request.form["nom_utilisateur"]
        mot_de_passe = request.form["mot_de_passe"]
        email = request.form["email"]

        if Utilisateur.exist(id_utilisateur):
            flash("Utilisateur avec cet ID existe déjà.", "error")
            return redirect(url_for("users.register"))
        else:
            nouvel_utilisateur = Utilisateur(
                id_utilisateur=id_utilisateur,
                nom_utilisateur=nom_utilisateur,
                mot_de_passe=mot_de_passe,
                email=email,
            )
            flash(nouvel_utilisateur.register(), "success")
            return redirect(url_for("users.login"))



@utilisateur_routes.route("/deconnexion", methods=["GET"])
def deconnexion():
    # Supprimer la clé 'logged_in' de la session
    session.pop("logged_in", None)
    # Supprimer le nom d'utilisateur de la session
    session.pop("username", None)
    # Supprimer l'id utilisateur de la session
    session.pop("user_id", None)

    return redirect(url_for("users.login"))  # Rediriger vers la page de connexion




@utilisateur_routes.route("/supprimer_utilisateur", methods=["GET", "POST"])
def supprimer_utilisateur():
    if request.method == "GET":
        return render_template(
            "supprimer_utilisateur.html", utilisateurs=Utilisateur.get_users()
        )
    else:
        utilisateur_id = request.form["utilisateur_id"]  # Get the utilisateur_id from the form
        Utilisateur.supprimer_utilisateur(utilisateur_id)  # Pass utilisateur_id as an argument
        flash("Utilisateur supprimé avec ses éléments associés.", "success")
        return redirect(url_for("users.supprimer_utilisateur"))
