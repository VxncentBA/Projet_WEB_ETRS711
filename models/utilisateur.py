import sqlite3
import bcrypt


class Utilisateur:
    def __init__(self, id_utilisateur, nom_utilisateur, mot_de_passe, email):
        # Attributs d'un utilisateur
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email

    # Methode pour crée un utilisateur
    def register(self):
        hashed_password = bcrypt.hashpw(
            self.mot_de_passe.encode("utf-8"), bcrypt.gensalt()
        )

        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO Utilisateurs VALUES (?, ?, ?, ?)",
            (self.id_utilisateur, self.nom_utilisateur, hashed_password, self.email),
        )
        conn.commit()
        conn.close()

        return "Nouvel utilisateur créé avec succès"

    # Méthode pour connecter un utilisateur
    @staticmethod
    def login():
        pass

    @staticmethod
    def exist(id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM Utilisateurs WHERE id_utilisateur = ?", (id,)
        )
        utilisateur = c.fetchone()
        conn.close()
        return utilisateur is not None

    @staticmethod
    def get_user_by_username(nom_utilisateur):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute(
            "SELECT id_utilisateur, nom_utilisateur, mot_de_passe FROM Utilisateurs WHERE nom_utilisateur = ?",
            (nom_utilisateur,),
        )
        utilisateur = c.fetchone()
        conn.close()
        return utilisateur

    @staticmethod
    def get_users():
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT id_utilisateur, nom_utilisateur FROM Utilisateurs")
        utilisateurs = c.fetchall()
        conn.close()

        return utilisateurs

    @staticmethod
    def supprimer_utilisateur(utilisateur_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()

        c.execute(
            "DELETE FROM Etageres WHERE cave_associee_id IN (SELECT id_cave FROM Caves WHERE proprietaire_id = ?)",
            (utilisateur_id,),
        )
        c.execute(
            "DELETE FROM Bouteilles WHERE id_bouteille IN (SELECT id_bouteille FROM Etageres WHERE cave_associee_id IN (SELECT id_cave FROM Caves WHERE proprietaire_id = ?))",
            (utilisateur_id,),
        )
        c.execute("DELETE FROM Caves WHERE proprietaire_id = ?", (utilisateur_id,))
        c.execute(
            "DELETE FROM Utilisateurs WHERE id_utilisateur = ?",
            (utilisateur_id,),
        )

        conn.commit()
        conn.close()
        return "Utilisateur supprimé avec ses éléments associés"
