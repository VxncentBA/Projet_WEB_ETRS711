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
        return nouvelle_etagere


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



class Etagere:
    def __init__(self, id_etagere, numero, region, emplacements_disponibles, cave_associee):
        # Attributs d'une étagère
        self.id_etagere = id_etagere
        self.numero = numero
        self.region = region
        self.emplacements_disponibles = emplacements_disponibles
        self.cave_associee = cave_associee
        self.bouteilles = []  # Liste pour stocker les bouteilles


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

# Création d'utilisateurs
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
utilisateur2 = Utilisateur(2, "Bob", "mdp456", "bob@email.com")

# Création de caves pour les utilisateurs
cave1 = utilisateur1.creer_cave(1, "Cave d'Alice")
cave2 = utilisateur2.creer_cave(2, "Cave de Bob")
cave3 = utilisateur1.creer_cave(1, "Cave d'Alice 2")

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


# Création de bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(2, "Domaine B", "Vin Blanc", "Blanc", 2015, "Bourgogne", "Très bon vin", "17/20", "13/20", "photo2.jpg", 40.0)
bouteille3 = Bouteille(3, "Domaine C", "Vin Rosé", "Rosé", 2020, "Provence", "Fruité et léger", "16/20", "14/20", "photo3.jpg", 30.0)

# Ajout de bouteilles aux caves en utilisant la méthode ajouter_bouteille
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille2)
cave2.ajouter_bouteille(bouteille3)
cave3.ajouter_bouteille(bouteille3)
cave3.ajouter_bouteille(bouteille3)

# Consultation du contenu des caves
print("Contenu de la Cave d'Alice:")
cave1.consulter_quantite_bouteilles_cave(utilisateur1)

print("\nContenu de la Cave de Bob:")
cave2.consulter_quantite_bouteilles_cave(utilisateur2)
