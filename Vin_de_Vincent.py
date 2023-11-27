import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def accueil():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Utilisateurs")
    utilisateurs = c.fetchall()
    conn.close()
    return render_template('accueil.html', utilisateurs=utilisateurs)

@app.route('/tables')
def afficher_tables():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()

    # Récupération des données de la table Utilisateurs
    c.execute("SELECT * FROM Utilisateurs")
    utilisateurs = c.fetchall()

    # Récupération des données de la table Caves
    c.execute("SELECT * FROM Caves")
    caves = c.fetchall()

    # Récupération des données de la table Etageres
    c.execute("SELECT * FROM Etageres")
    etageres = c.fetchall()

    # Récupération des données de la table Bouteilles
    c.execute("SELECT * FROM Bouteilles")
    bouteilles = c.fetchall()

    conn.close()

    return render_template('affichage_tables.html', utilisateurs=utilisateurs, caves=caves, etageres=etageres, bouteilles=bouteilles)


if __name__ == '__main__':
    app.run(debug=True)

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

    def creer_etagere(self, id_etagere, numero_etagere, region, emplacements_disponibles, cave_associee):
        # Crée une nouvelle étagère et l'ajoute à la liste des étagères de l'utilisateur
        nouvelle_etagere = Etagere(id_etagere, numero_etagere, region, emplacements_disponibles, cave_associee)
        self.etageres.append(nouvelle_etagere)
        cave_associee.etageres.append(nouvelle_etagere)  # Ajout à la liste des étagères de la cave
        print(cave_associee)
        return nouvelle_etagere
    
    def sauvegarder_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("INSERT INTO Utilisateurs VALUES (?, ?, ?, ?)",
                  (self.id_utilisateur, self.nom_utilisateur, self.mot_de_passe, self.email))
        conn.commit()
        conn.close()


class Cave:
    def __init__(self, id_cave, nom_cave, proprietaire):
        # Attributs d'une cave
        self.id_cave = id_cave
        self.nom_cave = nom_cave
        self.proprietaire = proprietaire
        self.etageres = []  # Liste pour stocker les étagères
        self.bouteilles = []  # Liste pour stocker les bouteilles

    def consulter_quantite_bouteilles_cave(self, utilisateur):
        if not utilisateur.caves:
            print("Aucune cave disponible pour cet utilisateur.")
            return
    
        print("Caves disponibles:")
        for i, cave in enumerate(utilisateur.caves, start=1):
            print(f"{i}. {cave.nom_cave}")

        choix_cave = int(input("Entrez le numéro de la cave à consulter : ")) - 1

        if 0 <= choix_cave < len(utilisateur.caves):
            cave_a_consulter = utilisateur.caves[choix_cave]
            self.afficher_details_cave(cave_a_consulter)
        else:
            print("Numéro de cave invalide.")

    def afficher_details_cave(self, cave):
        print(f"Nom de la cave : {cave.nom_cave}")
        print("Étagères dans cette cave :")
        for etagere in cave.etageres:
            print(f"Numéro de l'étagère : {etagere.numero}")
            print(f"Région de l'étagère : {etagere.region}")
            print(f"Emplacements disponibles : {etagere.emplacements_disponibles}")

            if etagere.bouteilles:
                print("Bouteilles sur cette étagère :")
                bouteilles_count = {}
                for bouteille in etagere.bouteilles:
                    if bouteille.nom not in bouteilles_count:
                        bouteilles_count[bouteille.nom] = 1
                    else:
                        bouteilles_count[bouteille.nom] += 1

                for nom, quantite in bouteilles_count.items():
                    print(f"- {nom} : {quantite} bouteille(s)")
            else:
                print("Aucune bouteille sur cette étagère.")

            print()  # Pour l'affichage clair entre les étagères
    
    def ajouter_bouteille(self, bouteille):
        region_bouteille = bouteille.region

        for etagere in self.etageres:
            if etagere.region == region_bouteille and etagere.emplacements_disponibles > 0:
                etagere.bouteilles.append(bouteille)
                etagere.emplacements_disponibles -= 1
                self.bouteilles.append(bouteille)  # Ajout à la liste de bouteilles de la cave
                print(f"Bouteille ajoutée à l'étagère {etagere.numero} dans la cave {self.nom_cave}.")
                return True

        print(f"Aucune étagère disponible dans la région {region_bouteille} de la cave {self.nom_cave}.")
        return False

    def supprimer_bouteille(self, bouteille):
        for etagere in self.etageres:
            if bouteille in etagere.bouteilles:
                etagere.bouteilles.remove(bouteille)
                etagere.emplacements_disponibles += 1  # Augmenter le nombre d'emplacements disponibles
                self.bouteilles.remove(bouteille)
                print(f"Bouteille '{bouteille.nom}' supprimée de l'étagère {etagere.numero} dans la cave {self.nom_cave}.")
                return True
        
        if bouteille in self.bouteilles:
            self.bouteilles.remove(bouteille)
            print(f"Bouteille '{bouteille.nom}' supprimée de la cave {self.nom_cave}.")
            return True
        
        print(f"Bouteille '{bouteille.nom}' introuvable dans la cave {self.nom_cave}.")
        return False
    
    def sauvegarder_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("INSERT INTO Caves VALUES (?, ?, ?)",
                  (self.id_cave, self.nom_cave, self.proprietaire.id_utilisateur))
        conn.commit()
        conn.close()



class Etagere:
    def __init__(self, id_etagere, numero, region, emplacements_disponibles, cave_associee):
        # Attributs d'une étagère
        self.id_etagere = id_etagere
        self.numero = numero
        self.region = region
        self.emplacements_disponibles = emplacements_disponibles
        self.cave_associee = cave_associee
        self.bouteilles = []  # Liste pour stocker les bouteilles

    def sauvegarder_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()

        # Vérifier si l'id_etagere existe déjà dans la table
        c.execute("SELECT id_etagere FROM Etageres WHERE id_etagere = ?", (self.id_etagere,))
        existing_id = c.fetchone()

        if existing_id is None:
            # Si l'ID n'existe pas, insérer la nouvelle étagère
            c.execute("INSERT INTO Etageres VALUES (?, ?, ?, ?, ?)",
                      (self.id_etagere, self.numero, self.region, self.emplacements_disponibles, self.cave_associee.id_cave))
            conn.commit()
            conn.close()
            print("Étagère ajoutée avec succès à la base de données.")
        else:
            print("ID d'étagère déjà existant dans la base de données. Étagère non ajoutée.")
    


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

    def consulter_quantite_bouteilles_cave(self, utilisateur):
        if not self.bouteilles:  # Vérification si la cave a des bouteilles
            print(f"Aucune bouteille dans la cave {self.nom_cave}.")
            return

        print(f"Nom de la cave : {self.nom_cave}")
        print("Bouteilles dans cette cave :")
        bouteilles_count = {}  # Dictionnaire pour stocker le nombre de bouteilles par nom
        for bouteille in self.bouteilles:
            if bouteille.nom not in bouteilles_count:
                bouteilles_count[bouteille.nom] = 1
            else:
                bouteilles_count[bouteille.nom] += 1

        for nom, quantite in bouteilles_count.items():
            print(f"- {nom} : {quantite} bouteille(s)")
    
    def archiver_bouteille(self, note_archivage):
        self.note_archivage = note_archivage
        print(f"Bouteille '{self.nom}' archivée avec la note : {note_archivage}")

    
    def sauvegarder_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("INSERT INTO Bouteilles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.id_bouteille, self.domaine_viticole, self.nom, self.type, self.annee,
                   self.region, self.commentaires, self.note_personnelle, self.note_moyenne,
                   self.photo_etiquette, self.prix))
        conn.commit()
        conn.close()

# Création d'utilisateurs
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
utilisateur2 = Utilisateur(2, "Bob", "mdp456", "bob@email.com")

utilisateur3 = Utilisateur(3, "Mathis", "mdp456", "bob@email.com")


# Appel des méthodes pour sauvegarder les utilisateurs dans la base de données
# utilisateur1.sauvegarder_dans_bdd()
# utilisateur2.sauvegarder_dans_bdd()
# utilisateur3.sauvegarder_dans_bdd()

# Création de caves pour les utilisateurs
cave1 = utilisateur1.creer_cave(1, "Cave d'Alice")
cave2 = utilisateur2.creer_cave(2, "Cave de Bob")
cave3 = utilisateur1.creer_cave(3, "Cave d'Alice 2")
cave4 = utilisateur3.creer_cave(4, "Cave de Mathis")

# Enregistrement des caves dans la base de données
# cave1.sauvegarder_dans_bdd()
# cave2.sauvegarder_dans_bdd()
# cave3.sauvegarder_dans_bdd()
# cave4.sauvegarder_dans_bdd()

# Création d'étagères dans les caves
etagere1 = utilisateur1.creer_etagere(1, 1, "Bordeaux", 30, cave1)
etagere2 = utilisateur1.creer_etagere(2, 1, "Bourgogne", 40, cave1)
etagere3 = utilisateur1.creer_etagere(3, 1, "Provence", 40, cave1)


etagere4 = utilisateur2.creer_etagere(4, 1, "Bordeaux", 30, cave2)
etagere5 = utilisateur2.creer_etagere(5, 1, "Bourgogne", 40, cave2)
etagere6 = utilisateur2.creer_etagere(6, 1, "Provence", 40, cave2)


etagere7 = utilisateur1.creer_etagere(7, 1, "Bordeaux", 30, cave3)
etagere8 = utilisateur1.creer_etagere(8, 1, "Bourgogne", 40, cave3)
etagere9 = utilisateur1.creer_etagere(9, 1, "Provence", 40, cave3)

etagere10 = utilisateur3.creer_etagere(10, 1, "Provence", 10, cave4)



# Enregistrement des étagères dans la base de données
# etagere1.sauvegarder_dans_bdd()
# etagere2.sauvegarder_dans_bdd()
# etagere3.sauvegarder_dans_bdd()
# etagere4.sauvegarder_dans_bdd()
# etagere5.sauvegarder_dans_bdd()
# etagere6.sauvegarder_dans_bdd()
# etagere7.sauvegarder_dans_bdd()
# etagere8.sauvegarder_dans_bdd()
# etagere9.sauvegarder_dans_bdd()
# etagere10.sauvegarder_dans_bdd()


# Création de bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(2, "Domaine B", "Vin Blanc", "Blanc", 2015, "Bourgogne", "Très bon vin", "17/20", "13/20", "photo2.jpg", 40.0)
bouteille3 = Bouteille(3, "Domaine C", "Vin Rosé", "Rosé", 2020, "Provence", "Fruité et léger", "16/20", "14/20", "photo3.jpg", 30.0)

# Appel des méthodes pour sauvegarder les bouteilles dans la base de données
# bouteille1.sauvegarder_dans_bdd()
# bouteille2.sauvegarder_dans_bdd()
# bouteille3.sauvegarder_dans_bdd()

# Ajout de bouteilles aux caves en utilisant la méthode ajouter_bouteille
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille2)
cave2.ajouter_bouteille(bouteille3)
cave3.ajouter_bouteille(bouteille3)
cave3.ajouter_bouteille(bouteille3)


cave4.ajouter_bouteille(bouteille3)

# Consultation du contenu des caves
print("Contenu de la Cave d'Alice:")
cave1.consulter_quantite_bouteilles_cave(utilisateur1)


# Supprimer une bouteille
cave1.supprimer_bouteille(bouteille1)

# Archiver une bouteille
bouteille3.archiver_bouteille("Bonne, mais pas exceptionnelle.")

# Consultation du contenu des caves
print("Contenu de la Cave d'Alice:")
cave1.consulter_quantite_bouteilles_cave(utilisateur1)

print("\nContenu de la Cave de Bob:")
cave2.consulter_quantite_bouteilles_cave(utilisateur2)


# Consultation du contenu des caves
print("Contenu de la Cave de Mathis:")
cave4.consulter_quantite_bouteilles_cave(utilisateur3)