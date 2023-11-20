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

    def creer_etagere(self, id_etagere, numero_etagere, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee):
        # Crée une nouvelle étagère et l'ajoute à la liste des étagères de l'utilisateur
        nouvelle_etagere = Etagere(id_etagere, numero_etagere, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee)
        self.etageres.append(nouvelle_etagere)
        return nouvelle_etagere


class Cave:
    def __init__(self, id_cave, nom_cave, proprietaire):
        # Attributs d'une cave
        self.id_cave = id_cave
        self.nom_cave = nom_cave
        self.proprietaire = proprietaire  # L'utilisateur propriétaire de la cave
        # Listes pour stocker les étagères et les bouteilles de la cave
        self.etageres = []
        self.bouteilles = []

    def ajouter_etagere(self, etagere):
        # Ajoute une étagère à la liste des étagères de la cave
        self.etageres.append(etagere)

    def ajouter_bouteille(self, bouteille, quantite):
        for etagere in self.etageres:
            if quantite <= 0:
                break
            
            quantite_restante = etagere.emplacements_disponibles - etagere.nombre_bouteilles
            if quantite_restante > 0:
                ajout = min(quantite, quantite_restante)
                etagere.ajouter_bouteille(bouteille, ajout)
                quantite -= ajout
                print(f"Il reste {quantite} bouteille(s) à ajouter")
        
        if quantite > 0:
            print(f"Impossible d'ajouter {quantite} bouteille(s), emplacements insuffisants dans les étagères")

    def retirer_bouteille(self, bouteille, archiver=False, note_archivage=""):
        # Retire une bouteille de la cave (possibilité de l'archiver avec une note)
        if bouteille in self.bouteilles:
            if archiver:
                print(f"Bouteille archivée avec la note: {note_archivage}")
                self.bouteilles.remove(bouteille)
            else:
                self.bouteilles.remove(bouteille)
                print("Bouteille supprimée de la cave")
        else:
            print("La bouteille spécifiée n'est pas présente dans la cave")
    
    def consulter(self):
        # Affiche le nombre total de bouteilles dans la cave et la quantité par type de vin
        infos_bouteilles_par_type = {}
        total_bouteilles = 0

        for bouteille in self.bouteilles:
            if bouteille.type not in infos_bouteilles_par_type:
                infos_bouteilles_par_type[bouteille.type] = 0
            infos_bouteilles_par_type[bouteille.type] += 1
            total_bouteilles += 1

        print(f"Contenu de la cave '{self.nom_cave}':")
        print("Nombre total de bouteilles dans la cave:", total_bouteilles)
        print("\nQuantité par type de vin dans la cave:")
        for vin, quantite in infos_bouteilles_par_type.items():
            print(f"Type de vin '{vin}': Quantité = {quantite}")


class Etagere:
    def __init__(self, id_etagere, numero, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee):
        # Attributs d'une étagère
        self.id_etagere = id_etagere
        self.numero = numero
        self.region = region
        self.emplacements_disponibles = emplacements_disponibles
        self.bouteilles_par_etagere = bouteilles_par_etagere
        self.emplacements = [None] * emplacements_disponibles  # Liste des emplacements, initialisée avec None (vide)
        self.nombre_bouteilles = 0
        self.cave_associee = cave_associee  # Association avec une cave

    def ajouter_bouteille(self, bouteille, quantite):
        # Ajoute une quantité spécifique de bouteilles à une étagère
        for i in range(len(self.emplacements)):
            if self.nombre_bouteilles < self.emplacements_disponibles and quantite > 0:
                if self.emplacements[i] is None:
                    self.emplacements[i] = bouteille
                    self.nombre_bouteilles += 1
                    print(f"Bouteille ajoutée à l'emplacement {i} de l'étagère {self.numero}")
                    quantite -= 1
                else:
                    print(f"L'emplacement {i} de l'étagère {self.numero} est déjà occupé")
        
        if quantite > 0:
            print(f"Impossible d'ajouter {quantite} bouteille(s), emplacements insuffisants")

    def supprimer_bouteille(self, quantite):
        # Supprime une quantité spécifique de bouteilles de l'étagère
        removed_count = 0

        for i in range(len(self.emplacements)):
            if removed_count < quantite and self.emplacements[i] is not None:
                self.emplacements[i] = None
                self.nombre_bouteilles -= 1
                print(f"Bouteille retirée de l'emplacement {i} de l'étagère {self.numero}")
                removed_count += 1
        
        if removed_count < quantite:
            print(f"Impossible de retirer {quantite - removed_count} bouteille(s), insuffisantes")


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


# Exemple de test


# Création d'utilisateurs
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
utilisateur2 = Utilisateur(2, "Bob", "mdp456", "bob@email.com")

# Création de caves pour les utilisateurs
cave1 = utilisateur1.creer_cave(1, "Cave d'Alice")
cave2 = utilisateur2.creer_cave(2, "Cave de Bob")

# Création d'étagères dans les caves
etagere1 = utilisateur1.creer_etagere(1, 1, "Bordeaux", 30, 20, cave1)
etagere2 = utilisateur2.creer_etagere(2, 1, "Bourgogne", 40, 10, cave2)


# Création de bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(2, "Domaine B", "Vin Blanc", "Blanc", 2015, "Bourgogne", "Très bon vin", "17/20", "13/20", "photo2.jpg", 40.0)

# Ajout de bouteilles aux caves
cave1.ajouter_bouteille(bouteille1, 10)  # Ajout de 10 bouteilles de bouteille1
cave2.ajouter_bouteille(bouteille2, 5)  # Ajout de 5 bouteilles de bouteille2


# Consultation du contenu des caves
print("Contenu de la Cave d'Alice:")
cave1.consulter()

print("\nContenu de la Cave de Bob:")
cave2.consulter()

# Retrait d'une bouteille d'une étagère
etagere1.supprimer_bouteille(0)

# Consultation à nouveau du contenu de la Cave d'Alice après suppression d'une bouteille
print("\nContenu de la Cave d'Alice après suppression d'une bouteille:")
cave1.consulter()
