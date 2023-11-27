import sqlite3
def vider_bdd():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    c = conn.cursor()

    # Supprimer toutes les lignes des tables
    tables = ['Utilisateurs', 'Caves', 'Etageres', 'Bouteilles']
    for table in tables:
        c.execute(f"DELETE FROM {table}")

    conn.commit()
    conn.close()