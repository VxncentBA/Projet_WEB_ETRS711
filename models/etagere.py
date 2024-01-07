import sqlite3
from models.bouteille import Bouteille

class Etagere:
    def __init__(self, id_etagere, numero, region, capacite, cave_associee):
        self.id_etagere = id_etagere
        self.numero = numero
        self.region = region
        self.capacite = capacite
        self.cave_associee = cave_associee
        self.bouteilles = []  # Ajout de l'attribut pour les bouteilles
        self.charger_bouteilles()  # Chargement des bouteilles

    def to_dict(self):
        bouteilles = []
        print(self.bouteilles)
        if self.bouteilles != [] or self.bouteilles != None:
            for bottle in self.bouteilles:
                bouteilles.append(bottle.to_dict())

        return {
            "id_etagere": self.id_etagere,
            "numero": self.numero,
            "region": self.region,
            "capacite": self.capacite,
            "cave_associee": self.cave_associee,
            "bouteilles": bouteilles,
        }

    @staticmethod
    def get_etageres():
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres")
        rows = c.fetchall()
        etageres = [
            Etagere(row[0], row[1], row[2], row[3], row[4]) for row in rows
        ]
        conn.close()
        return etageres

    @staticmethod
    def obtenir_dernier_id_etagere():
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT MAX(id_etagere) FROM Etageres")
        dernier_id_etagere = c.fetchone()[0]
        conn.close()
        return dernier_id_etagere

    def INSERT(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("INSERT INTO Etageres VALUES (?, ?, ?, ?, ?)",
                  (self.id_etagere, self.numero, self.region, self.capacite, self.cave_associee.id_cave))
        conn.commit()
        conn.close()

    def UPDATE(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("UPDATE Etageres SET numero = ?, region = ?, capacite = ?, cave_associee_id = ? WHERE id_etagere = ?",
                  (self.numero, self.region, self.capacite, self.cave_associee.id_cave, self.id_etagere))
        conn.commit()
        conn.close()

    def DELETE(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("DELETE FROM Etageres WHERE id_etagere = ?", (self.id_etagere,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_etagere_by_id(id_etagere):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres WHERE id_etagere = ?", (id_etagere,))
        row = c.fetchone()
        etagere = Etagere(row[0], row[1], row[2], row[3])
        conn.close()
        return etagere

    @staticmethod
    def get_etageres_cave(cave_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres WHERE cave_associee_id = ?", (cave_id,))
        rows = c.fetchall()
        etageres = [
            Etagere(row[0], row[1], row[2], row[3]) for row in rows
        ]
        conn.close()
        return etageres

    @staticmethod
    def get_etageres_cave_by_id(cave_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres WHERE cave_associee_id = ?", (cave_id,))
        rows = c.fetchall()
        etageres = [
            Etagere(row[0], row[1], row[2], row[3]) for row in rows
        ]
        conn.close()
        return etageres

    @staticmethod
    def get_utilisateur_etageres(utilisateur_id):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres WHERE cave_associee_id IN (SELECT id_cave FROM Caves WHERE proprietaire_id = ?)", (utilisateur_id,))
        rows = c.fetchall()
        etageres = [
            Etagere(row[0], row[1], row[2], row[3]) for row in rows
        ]
        conn.close()
        return etageres

    @staticmethod
    def get_etagere_details(id_etagere):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Etageres WHERE id_etagere = ?", (id_etagere,))
        row = c.fetchone()
        etagere = Etagere(row[0], row[1], row[2], row[3])
        conn.close()
        return etagere

    @staticmethod
    def ajouter_bouteille_etagere(id_bouteille, id_etagere):
        id=Etagere.obtenir_dernier_id_etagerebouteille()+1
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("INSERT INTO EtagereBouteille VALUES (?, ?, ?)", (id, id_bouteille, id_etagere))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_bouteille_etagere(id_bouteille, id_etagere):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("DELETE FROM EtagereBouteille WHERE bouteille_id = ? AND etagere_id = ?", (id_etagere, id_bouteille))
        conn.commit()
        conn.close()

    @staticmethod
    def obtenir_dernier_id_etagerebouteille():
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM EtagereBouteille")
        dernier_id_etagerebouteille = c.fetchone()[0]
        conn.close()
        return dernier_id_etagerebouteille

    @staticmethod
    def get_emplacement_utilises(id_etagere):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM EtagereBouteille WHERE etagere_id = ?", (id_etagere,))
        emplacements_utilises = c.fetchone()[0]
        conn.close()
        return emplacements_utilises

    @staticmethod
    def get_emplacement_disponibles(id_etagere):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute("SELECT emplacements_disponibles FROM Etageres WHERE id_etagere = ?", (id_etagere,))
        capacite = c.fetchone()[0]
        conn.close()
        return capacite - Etagere.get_emplacement_utilises(id_etagere)

    def charger_bouteilles(self):
        conn = sqlite3.connect("bdd.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM Bouteilles WHERE id_bouteille IN (SELECT bouteille_id FROM EtagereBouteille WHERE etagere_id = ?)", 
            (self.id_etagere,)
        )
        rows = c.fetchall()
        for row in rows:
            bouteille = Bouteille(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            self.bouteilles.append(bouteille)
        conn.close()
