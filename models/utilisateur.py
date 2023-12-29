import sqlite3


class Utilisateur:
    def __init__(self, id_utilisateur, nom_utilisateur, mot_de_passe, email):
        # Attributs d'un utilisateur
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email
        # Listes pour stocker les caves et les étagères de l'utilisateur
        self.caves = []
        self.etageres = []

    def creer_cave(self, id_cave, nom_cave):
        # Crée une nouvelle cave et l'ajoute à la liste des caves de l'utilisateur
        nouvelle_cave = Cave(id_cave, nom_cave, self)
        self.caves.append(nouvelle_cave)
        return nouvelle_cave

    def creer_etagere(
        self,
        id_etagere,
        numero_etagere,
        region,
        emplacements_disponibles,
        cave_associee,
    ):
        # Crée une nouvelle étagère et l'ajoute à la liste des étagères de l'utilisateur
        nouvelle_etagere = Etagere(
            id_etagere, numero_etagere, region, emplacements_disponibles, cave_associee
        )
        self.etageres.append(nouvelle_etagere)
        cave_associee.etageres.append(
            nouvelle_etagere
        )  # Ajout à la liste des étagères de la cave
        print(cave_associee)
        return nouvelle_etagere

    def sauvegarder_dans_bdd(self):
        conn = sqlite3.connect("ma_base_de_donnees.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO Utilisateurs VALUES (?, ?, ?, ?)",
            (self.id_utilisateur, self.nom_utilisateur, self.mot_de_passe, self.email),
        )
        conn.commit()
        conn.close()

    def mettre_a_jour_dans_bdd(self):
        conn = sqlite3.connect("ma_base_de_donnees.db")
        c = conn.cursor()
        c.execute(
            "UPDATE Utilisateurs SET nom_utilisateur = ?, mot_de_passe = ?, email = ? WHERE id_utilisateur = ?",
            (self.nom_utilisateur, self.mot_de_passe, self.email, self.id_utilisateur),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def utilisateur_existe(id_utilisateur):
        conn = sqlite3.connect("ma_base_de_donnees.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM Utilisateurs WHERE id_utilisateur = ?", (id_utilisateur,)
        )
        utilisateur = c.fetchone()
        conn.close()
        return utilisateur is not None
