class Utilisateur:
    def __init__(self, id_utilisateur, nom_utilisateur, mot_de_passe, email):
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email
        self.caves = []
        self.etageres = []

    def creer_cave(self, id_cave, nom_cave):
        nouvelle_cave = Cave(id_cave, nom_cave, self)
        self.caves.append(nouvelle_cave)
        return nouvelle_cave

    def creer_etagere(self, id_etagere, numero_etagere, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee):
        nouvelle_etagere = Etagere(id_etagere, numero_etagere, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee)
        self.etageres.append(nouvelle_etagere)
        return nouvelle_etagere


class Cave:
    def __init__(self, id_cave, nom_cave, proprietaire):
        self.id_cave = id_cave
        self.nom_cave = nom_cave
        self.proprietaire = proprietaire
        self.etageres = []
        self.bouteilles = []

    def ajouter_etagere(self, etagere):
        self.etageres.append(etagere)

    def ajouter_bouteille(self, bouteille):
        self.bouteilles.append(bouteille)
    
    def consulter(self):
        infos_bouteilles = {}
        for bouteille in self.bouteilles:
            total_quantite = sum([lot.quantite for lot in bouteille.lots])
            infos_bouteilles[bouteille.id_bouteille] = {
                "nom": bouteille.nom,
                "quantite": total_quantite
            }
        return infos_bouteilles

    # Méthode pour afficher la quantité actuelle pour chaque bouteille dans la cave
    def afficher_quantite_bouteilles(self):
        infos_bouteilles = self.consulter()

        print("Quantité actuelle pour chaque bouteille dans la cave:")
        for bouteille_id, info in infos_bouteilles.items():
            print(f"Bouteille ID {bouteille_id}: Nom = {info['nom']}, Quantité = {info['quantite']}")


class Etagere:
    def __init__(self, id_etagere, numero_etagere, region, emplacements_disponibles, bouteilles_par_etagere, cave_associee):
        self.id_etagere = id_etagere
        self.numero_etagere = numero_etagere
        self.region = region
        self.emplacements_disponibles = emplacements_disponibles
        self.bouteilles_par_etagere = bouteilles_par_etagere
        self.cave_associee = cave_associee


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


class Lot:
    def __init__(self, id_lot, bouteille, quantite):
        self.id_lot = id_lot
        self.bouteille = bouteille
        self.quantite = quantite


# Exemple de test
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
cave1 = utilisateur1.creer_cave(1, "Ma Cave")
etagere1 = utilisateur1.creer_etagere(1, 1, "Bordeaux", 10, 20, cave1)

etagere2 = utilisateur1.creer_etagere(1, 1, "Lyon", 10, 20, cave1)


# Création des bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(1, "Domaine A", "Vin Blanc", "Blanc", 2010, "Lyon", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)

# Ajout des bouteilles à la cave
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille2)


# Création de lots associés à ces bouteilles
lot1 = Lot(1, bouteille1, 5)
lot2 = Lot(2, bouteille2, 3)

bouteille1.lots.append(lot1)
bouteille2.lots.append(lot2)

print("Utilisateur:", utilisateur1.nom_utilisateur)
print("Caves de l'utilisateur:", [cave.nom_cave for cave in utilisateur1.caves])
print("Etagères de l'utilisateur:", [etagere.numero_etagere for etagere in utilisateur1.etageres])
print("Bouteilles dans la cave 1:", [bouteille.nom for bouteille in cave1.bouteilles])
print("Nombre de lots pour la bouteille 1:", len(bouteille1.lots))

# Supposons que vous avez déjà créé une instance de la classe Cave nommée "cave1"
infos_bouteilles_cave1 = cave1.consulter()

# Affichage des informations sur les bouteilles dans la cave "cave1"
print("Quantité actuelle pour chaque bouteille dans la cave 'cave1':")
for bouteille_id, info in infos_bouteilles_cave1.items():
    print(f"Bouteille ID {bouteille_id}: Nom = {info['nom']}, Quantité = {info['quantite']}")

# Affichage de la quantité actuelle pour chaque bouteille dans la cave
cave1.afficher_quantite_bouteilles()
