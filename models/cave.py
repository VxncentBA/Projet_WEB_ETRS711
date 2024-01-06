import sqlite3
from models.etagere import Etagere
from models.utilisateur import Utilisateur


class Cave:
    def __init__(self, id_cave, nom_cave, proprietaire):
        # Attributs d'une cave
        self.id_cave = id_cave
        self.nom_cave = nom_cave
        self.proprietaire = proprietaire
        self.etageres = []  # Liste pour stocker les étagères
        self.bouteilles = []  # Liste pour stocker les bouteilles

    @staticmethod
    def get_utilisateur_caves(utilisateur_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Caves WHERE proprietaire_id = ?", (utilisateur_id,))
        rows = c.fetchall()
        caves_utilisateur = [
            Cave(row[0], row[1], Utilisateur(row[2], None, None, None)) for row in rows
        ]
        conn.close()
        return caves_utilisateur

    @classmethod
    def afficher_details_cave(cls, user_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()

        # Récupérer les caves de l'utilisateur connecté
        caves_utilisateur = Cave.get_utilisateur_caves(user_id)

        # Récupérer les étagères pour chaque cave de l'utilisateur
        for current_cave in caves_utilisateur:
            c.execute(
                "SELECT * FROM Etageres WHERE cave_associee_id = ?",
                (current_cave.id_cave,),
            )
            etageres_cave = c.fetchall()
            current_cave.etageres = [
                Etagere(row[0], row[1], row[2], row[3], current_cave)
                for row in etageres_cave
            ]

        conn.close()

        return caves_utilisateur

    def ajouter_bouteille(self, bouteille):
        region_bouteille = bouteille.region

        for etagere in self.etageres:
            if (
                etagere.region == region_bouteille
                and etagere.emplacements_disponibles > 0
            ):
                etagere.bouteilles.append(bouteille)
                etagere.emplacements_disponibles -= 1
                self.bouteilles.append(
                    bouteille
                )  # Ajout à la liste de bouteilles de la cave
                etagere.mettre_a_jour_emplacements_disponibles()  # Mettre à jour la BDD
                print(
                    f"Bouteille ajoutée à l'étagère {etagere.numero} dans la cave {self.nom_cave}."
                )
                return True

        print(
            f"Aucune étagère disponible dans la région {region_bouteille} de la cave {self.nom_cave}."
        )
        return False

    def supprimer_bouteille(self, bouteille):
        for etagere in self.etageres:
            if bouteille in etagere.bouteilles:
                etagere.bouteilles.remove(bouteille)
                etagere.emplacements_disponibles += (
                    1  # Augmenter le nombre d'emplacements disponibles
                )
                self.bouteilles.remove(bouteille)
                etagere.mettre_a_jour_emplacements_disponibles()  # Mettre à jour la BDD
                print(
                    f"Bouteille '{bouteille.nom}' supprimée de l'étagère {etagere.numero} dans la cave {self.nom_cave}."
                )
                return True

        if bouteille in self.bouteilles:
            self.bouteilles.remove(bouteille)
            print(f"Bouteille '{bouteille.nom}' supprimée de la cave {self.nom_cave}.")
            return True

        print(f"Bouteille '{bouteille.nom}' introuvable dans la cave {self.nom_cave}.")
        return False

    @staticmethod
    def obtenir_dernier_id_cave():
        conn = sqlite3.connect("ma_base_de_donnees.db")
        c = conn.cursor()
        c.execute("SELECT MAX(id_cave) FROM Caves")
        dernier_id = c.fetchone()[0]
        conn.close()
        return dernier_id if dernier_id else 0
