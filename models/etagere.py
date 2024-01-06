import sqlite3


class Etagere:
    def __init__(self, id_etagere, numero, region, capacite, cave_associee):
        self.id_etagere = id_etagere
        self.numero = numero
        self.region = region
        self.capacite = capacite
        self.cave_associee = cave_associee


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