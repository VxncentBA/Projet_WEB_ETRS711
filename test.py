import sqlite3
from Vin_de_Vincent import *


# Création d'utilisateurs
utilisateur1 = Utilisateur(1, "Alice", "motdepasse123", "alice@email.com")
utilisateur2 = Utilisateur(2, "Bob", "mdp456", "bob@email.com")
utilisateur3 = Utilisateur(3, "Mathis", "mdp456", "bob@email.com")


# Appel des méthodes pour sauvegarder les utilisateurs dans la base de données
#utilisateur1.sauvegarder_dans_bdd()
# utilisateur2.sauvegarder_dans_bdd()
# utilisateur3.sauvegarder_dans_bdd()

#utilisateur1.mettre_a_jour_dans_bdd()
utilisateur2.mettre_a_jour_dans_bdd()
utilisateur3.mettre_a_jour_dans_bdd()



# Création de caves pour les utilisateurs
cave1 = utilisateur1.creer_cave(1, "Cave d'Alice")
cave2 = utilisateur2.creer_cave(2, "Cave de Bob")
cave3 = utilisateur1.creer_cave(3, "Cave d'Alice 2")
cave4 = utilisateur3.creer_cave(4, "Cave de Mathis")

# Enregistrement des caves dans la base de données
#cave1.sauvegarder_dans_bdd()
cave2.mettre_a_jour_dans_bdd()
#cave3.sauvegarder_dans_bdd()
cave4.mettre_a_jour_dans_bdd()

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
etagere1.sauvegarder_dans_bdd()
etagere2.sauvegarder_dans_bdd()
etagere3.sauvegarder_dans_bdd()
etagere4.mettre_a_jour_dans_bdd()
etagere5.mettre_a_jour_dans_bdd()
etagere6.mettre_a_jour_dans_bdd()
etagere7.sauvegarder_dans_bdd()
etagere8.sauvegarder_dans_bdd()
etagere9.sauvegarder_dans_bdd()
etagere10.mettre_a_jour_dans_bdd()


# Création de bouteilles
bouteille1 = Bouteille(1, "Domaine A", "Vin Rouge", "Rouge", 2010, "Bordeaux", "Excellent vin", "18/20", "12/20", "photo1.jpg", 50.0)
bouteille2 = Bouteille(2, "Domaine B", "Vin Blanc", "Blanc", 2015, "Bourgogne", "Très bon vin", "17/20", "13/20", "photo2.jpg", 40.0)
bouteille3 = Bouteille(3, "Domaine C", "Vin Rosé", "Rosé", 2020, "Provence", "Fruité et léger", "16/20", "14/20", "photo3.jpg", 30.0)

# Appel des méthodes pour sauvegarder les bouteilles dans la base de données
#bouteille1.sauvegarder_dans_bdd()
bouteille1.mettre_a_jour_dans_bdd()
bouteille2.mettre_a_jour_dans_bdd()
bouteille3.mettre_a_jour_dans_bdd()

# Ajout de bouteilles aux caves en utilisant la méthode ajouter_bouteille
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille1)
cave1.ajouter_bouteille(bouteille1)
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