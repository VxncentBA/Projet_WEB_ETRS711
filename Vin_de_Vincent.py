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
        print("Bouteilles dans cette cave :")
        for bouteille in cave.bouteilles:
            print(f"- {bouteille.nom} ({bouteille.annee})")

        print(f"Nombre d'étagères dans cette cave : {len(cave.etageres)}")
        for etagere in cave.etageres:
            print(f"\nDétails de l'étagère {etagere.numero}:")
            print(f"  - Région : {etagere.region}")
            print(f"  - Emplacements disponibles : {etagere.emplacements_disponibles}")

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

    def consulter_quantite_bouteilles_cave(self):
        if not self.caves:
            print("Aucune cave disponible pour cet utilisateur.")
            return
        
        print("Caves disponibles:")
        for i, cave in enumerate(self.caves, start=1):
            print(f"{i}. {cave.nom_cave}")

        choix_cave = int(input("Entrez le numéro de la cave à consulter : ")) - 1

        if 0 <= choix_cave < len(self.caves):
            cave_a_consulter = self.caves[choix_cave]
            cave_a_consulter.consulter()
        else:
            print("Numéro de cave invalide.")

# Création d'utilisateurs
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
utilisateur2 = Utilisateur(2, "Bob", "mdp456", "bob@email.com")

# Création de caves pour les utilisateurs
cave1 = utilisateur1.creer_cave(1, "Cave d'Alice")
cave2 = utilisateur2.creer_cave(2, "Cave de Bob")
cave3 = utilisateur1.creer_cave(1, "Cave d'Alice 2")

# Création d'étagères dans les caves
etagere1 = utilisateur1.creer_etagere(1, 1, "Bordeaux", 30, cave1)
etagere2 = utilisateur2.creer_etagere(2, 1, "Bourgogne", 40, cave2)
etagere3 = utilisateur2.creer_etagere(2, 1, "Bourgogne", 40, cave3)

# Création de bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(2, "Domaine B", "Vin Blanc", "Blanc", 2015, "Bourgogne", "Très bon vin", "17/20", "13/20", "photo2.jpg", 40.0)
bouteille3 = Bouteille(3, "Domaine C", "Vin Rosé", "Rosé", 2020, "Provence", "Fruité et léger", "16/20", "14/20", "photo3.jpg", 30.0)

# Ajout de bouteilles aux caves
cave1.bouteilles.extend([bouteille1, bouteille2])
cave2.bouteilles.append(bouteille3)
cave3.bouteilles.append(bouteille3)
cave3.bouteilles.append(bouteille3)

# Consultation du contenu des caves
print("Contenu de la Cave d'Alice:")
cave1.consulter_quantite_bouteilles_cave(utilisateur1)

print("\nContenu de la Cave de Bob:")
cave2.consulter_quantite_bouteilles_cave(utilisateur2)