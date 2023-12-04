import sqlite3
from flask import Flask, render_template, request

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

    def mettre_a_jour_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("UPDATE Utilisateurs SET nom_utilisateur = ?, mot_de_passe = ?, email = ? WHERE id_utilisateur = ?",
                  (self.nom_utilisateur, self.mot_de_passe, self.email, self.id_utilisateur))
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
                etagere.mettre_a_jour_emplacements_disponibles()  # Mettre à jour la BDD
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
                etagere.mettre_a_jour_emplacements_disponibles()  # Mettre à jour la BDD
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

    def mettre_a_jour_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("UPDATE Caves SET nom_cave = ?, proprietaire_id = ? WHERE id_cave = ?", (self.nom_cave, self.proprietaire.id_utilisateur, self.id_cave))
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

    def mettre_a_jour_emplacements_disponibles(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("UPDATE Etageres SET emplacements_disponibles = ? WHERE id_etagere = ?",
                  (self.emplacements_disponibles, self.id_etagere))
        conn.commit()
        conn.close()

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

    def mettre_a_jour_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("UPDATE Etageres SET numero = ?, region = ?, emplacements_disponibles = ?, cave_associee_id = ? WHERE id_etagere = ?",
                  (self.numero, self.region, self.emplacements_disponibles, self.cave_associee.id_cave, self.id_etagere))
        conn.commit()
        conn.close()
    
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

    def mettre_a_jour_dans_bdd(self):
        conn = sqlite3.connect('ma_base_de_donnees.db')
        c = conn.cursor()
        c.execute("UPDATE Bouteilles SET domaine_viticole = ?, nom = ?, type = ?, annee = ?, region = ?, commentaires = ?, note_personnelle = ?, note_moyenne = ?, photo_etiquette = ?, prix = ? WHERE id_bouteille = ?",
                  (self.domaine_viticole, self.nom, self.type, self.annee, self.region, self.commentaires, self.note_personnelle, self.note_moyenne, self.photo_etiquette, self.prix, self.id_bouteille))
        conn.commit()
        conn.close()
