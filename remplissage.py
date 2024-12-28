############################# EXERCICE 1.2 #############################



import sqlite3
from datetime import datetime, timedelta

# Connexion à la base de données
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Charger et exécuter le script SQL depuis le fichier
with open('logement.sql', 'r') as f:
    sql_script = f.read()

# Exécuter le script SQL pour créer les tables et insérer les données
c.executescript(sql_script)

# Définir les valeurs des mesures (avec plusieurs mesures pour chaque capteur entre 2020 et 2024)
mesures = [
    ('2020-05-10', 22.5, 1),
    ('2020-06-15', 23.0, 1),
    ('2020-07-20', 21.8, 1),

    ('2021-01-10', 21.5, 1),
    ('2021-02-18', 22.0, 1),
    ('2021-03-25', 23.5, 1),

    ('2022-02-10', 24.0, 1),
    ('2022-03-15', 23.5, 1),
    ('2022-04-20', 22.2, 1),

    ('2023-01-15', 25.0, 1),
    ('2023-02-20', 24.5, 1),
    ('2023-03-05', 23.0, 1),

    ('2024-01-10', 22.5, 1),
    ('2024-01-15', 23.0, 1),
    ('2024-01-20', 21.8, 1),

    ('2020-05-01', 320.0, 2),
    ('2020-06-01', 315.0, 2),
    ('2020-07-10', 330.0, 2),

    ('2021-01-10', 310.0, 2),
    ('2021-02-15', 300.0, 2),
    ('2021-03-01', 320.0, 2),

    ('2022-02-10', 325.0, 2),
    ('2022-03-05', 335.0, 2),
    ('2022-04-10', 315.0, 2),

    ('2023-01-10', 310.0, 2),
    ('2023-02-20', 300.0, 2),
    ('2023-03-15', 320.0, 2),

    ('2024-01-10', 330.0, 2),
    ('2024-01-15', 315.0, 2),
    ('2024-01-20', 325.0, 2)
]

# Insertion des mesures dans la base de données
c.executemany("INSERT INTO Mesures (date_mesure, valeur, id_capteur) VALUES (?, ?, ?)", mesures)

# Définir les valeurs des factures (avec plusieurs factures, incluant Internet, entre 2020 et 2024)
factures = [
    ('Electricité', '2020-05-01', 120.50, 1),
    ('Eau', '2020-06-01', 50.25, 1),
    ('Gaz', '2020-07-10', 80.00, 1),
    ('Internet', '2020-08-15', 40.00, 1),
    ('Electricité', '2021-01-10', 130.50, 1),
    ('Eau', '2021-03-05', 55.75, 1),
    ('Gaz', '2021-04-18', 85.00, 1),
    ('Internet', '2021-06-01', 42.00, 1),
    ('Electricité', '2022-02-10', 140.00, 1),
    ('Eau', '2022-04-20', 60.50, 1),
    ('Gaz', '2022-05-25', 90.00, 1),
    ('Internet', '2022-07-01', 45.00, 1),
    ('Electricité', '2023-03-15', 150.00, 1),
    ('Eau', '2023-04-10', 65.00, 1),
    ('Gaz', '2023-05-20', 95.00, 1),
    ('Internet', '2023-07-10', 50.00, 1),
    ('Electricité', '2024-01-01', 100.50, 1),
    ('Eau', '2024-01-05', 30.25, 1),
    ('Gaz', '2024-01-10', 75.00, 1),
    ('Internet', '2024-01-15', 45.00, 1)
]

# Insertion des factures dans la base de données
c.executemany("INSERT INTO Facture (type, date_facture, montant, id_maison) VALUES (?, ?, ?, ?)", factures)

# Afficher les données pour vérifier l'insertion
c.execute('SELECT * FROM Mesures')
print("Mesures insérées :")
for row in c.fetchall():
    print(dict(row))

c.execute('SELECT * FROM Facture')
print("\nFactures insérées :")
for row in c.fetchall():
    print(dict(row))

# Fermeture de la connexion
conn.commit()
conn.close()