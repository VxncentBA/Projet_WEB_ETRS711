import sqlite3

def creer_bdd():
    # Création et connexion à la base de données
conn = sqlite3.connect('ma_base_de_donnees.db')
c = conn.cursor()

# Création de la table Utilisateurs
c.execute('''CREATE TABLE IF NOT EXISTS Utilisateurs (
                id_utilisateur INTEGER PRIMARY KEY,
                nom_utilisateur TEXT NOT NULL,
                mot_de_passe TEXT NOT NULL,
                email TEXT NOT NULL
            )''')

# Création de la table Caves
c.execute('''CREATE TABLE IF NOT EXISTS Caves (
                id_cave INTEGER PRIMARY KEY,
                nom_cave TEXT NOT NULL,
                proprietaire_id INTEGER NOT NULL,
                FOREIGN KEY (proprietaire_id) REFERENCES Utilisateurs(id_utilisateur)
            )''')

# Création de la table Etageres
c.execute('''CREATE TABLE IF NOT EXISTS Etageres (
                id_etagere INTEGER PRIMARY KEY,
                numero INTEGER NOT NULL,
                region TEXT NOT NULL,
                emplacements_disponibles INTEGER NOT NULL,
                cave_associee_id INTEGER NOT NULL,
                FOREIGN KEY (cave_associee_id) REFERENCES Caves(id_cave)
            )''')

# Création de la table Bouteilles
c.execute('''CREATE TABLE IF NOT EXISTS Bouteilles (
                id_bouteille INTEGER PRIMARY KEY,
                domaine_viticole TEXT NOT NULL,
                nom TEXT NOT NULL,
                type TEXT NOT NULL,
                annee INTEGER NOT NULL,
                region TEXT NOT NULL,
                commentaires TEXT,
                note_personnelle TEXT,
                note_moyenne TEXT,
                photo_etiquette TEXT,
                prix REAL
            )''')


# # Création de la table de liaison EtagereBouteille
# c.execute('''CREATE TABLE IF NOT EXISTS EtagereBouteille (
#                 id INTEGER PRIMARY KEY,
#                 etagere_id INTEGER NOT NULL,
#                 bouteille_id INTEGER NOT NULL,
#                 FOREIGN KEY (etagere_id) REFERENCES Etageres(id_etagere),
#                 FOREIGN KEY (bouteille_id) REFERENCES Bouteilles(id_bouteille)
#             )''')

# Commit pour sauvegarder les changements
conn.commit()

# Fermeture de la connexion
conn.close()

creer_bdd()