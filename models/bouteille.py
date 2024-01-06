import sqlite3


class Bouteille:
    def __init__(self, id_bouteille, domaine_viticole, nom, type, annee, region, commentaires, note_personnelle, note_moyenne, photo_etiquette, prix):
        self.id_bouteille = id_bouteille
        self.domaine_viticole = domaine_viticole
        self.nom = nom
        self.type = type
        self.annee = annee
        self.region = region
        self.commentaires = commentaires
        self.note_personnelle = note_personnelle
        self.note_moyenne = note_moyenne
        self.photo_etiquette = photo_etiquette
        self.prix = prix
        self.lots = []


    @staticmethod
    def get_bouteilles():
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Bouteilles")
        rows = c.fetchall()
        bouteilles_disponibles = []

        for row in rows:
            id_bouteille, domaine_viticole, nom, type, annee, region, commentaires, note_personnelle, note_moyenne, photo_etiquette, prix = row
            bouteille = Bouteille(
                id_bouteille=id_bouteille,
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
            bouteilles_disponibles.append(bouteille)

        conn.close()
        return bouteilles_disponibles

    @staticmethod
    def obtenir_dernier_id_bouteille():
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("SELECT MAX(id_bouteille) FROM Bouteilles")
        dernier_id_bouteille = c.fetchone()[0]
        conn.close()
        return dernier_id_bouteille

    def INSERT(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("INSERT INTO Bouteilles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.id_bouteille, self.domaine_viticole, self.nom, self.type, self.annee, self.region, self.commentaires, self.note_personnelle, self.note_moyenne, self.photo_etiquette, self.prix))
        conn.commit()
        conn.close()

    def UPDATE(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("UPDATE Bouteilles SET domaine_viticole = ?, nom = ?, type = ?, annee = ?, region = ?, commentaires = ?, note_personnelle = ?, note_moyenne = ?, photo_etiquette = ?, prix = ? WHERE id_bouteille = ?",
                  (self.domaine_viticole, self.nom, self.type, self.annee, self.region, self.commentaires, self.note_personnelle, self.note_moyenne, self.photo_etiquette, self.prix, self.id_bouteille))
        conn.commit()
        conn.close()

    def DELETE(self):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("DELETE FROM Bouteilles WHERE id_bouteille = ?", (self.id_bouteille,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_bouteille_by_id(id_bouteille):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Bouteilles WHERE id_bouteille = ?", (id_bouteille,))
        row = c.fetchone()
        bouteille = Bouteille(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        conn.close()
        return bouteille

    @staticmethod
    def get_bouteilles_by_etagere(id_etagere):
        conn = sqlite3.connect('bdd.db')
        c = conn.cursor()
        c.execute("SELECT Bouteilles.* FROM Bouteilles JOIN EtagereBouteille ON Bouteilles.id_bouteille = EtagereBouteille.id_bouteille WHERE EtagereBouteille.id_etagere = ?", (id_etagere,))
        rows = c.fetchall()
        bouteilles = []
        for row in rows:
            bouteille = Bouteille(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            bouteilles.append(bouteille)
        conn.close()
        return bouteilles
