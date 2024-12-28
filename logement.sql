-- Question 2 : Suppression des tables existantes

DROP TABLE IF EXISTS Mesures;
DROP TABLE IF EXISTS Capteurs;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Maison;
DROP TABLE IF EXISTS TypeCapteur;


-- Question 3 : Création des tables de la base de données
-- Création de la table Maison pour stocker les informations sur les maisons
CREATE TABLE IF NOT EXISTS Maison (
    id_maison INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    adresse_ip VARCHAR(15)
);

-- Création de la table Piece pour stocker les pièces d'une maison
CREATE TABLE IF NOT EXISTS Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50) NOT NULL,
    id_maison INTEGER,
    FOREIGN KEY (id_maison) REFERENCES Maison(id_maison) ON DELETE CASCADE
);

--Création de la table Capteurs pour stocker les informations sur les capteurs dans chaque pièce
CREATE TABLE IF NOT EXISTS Capteurs (
    id_capteur INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50) NOT NULL,
    port_com VARCHAR(20),
    reference VARCHAR(50),
    localisation VARCHAR(50),
    date_installation DATE,
    id_piece INTEGER,
    FOREIGN KEY (id_piece) REFERENCES Piece(id_piece) ON DELETE SET NULL
);

-- Création de la table TypeCapteur pour stocker les types de capteurs disponibles
CREATE TABLE IF NOT EXISTS TypeCapteur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50) NOT NULL
);

-- Création de la table Mesures pour stocker les mesures effectuées par les capteurs
CREATE TABLE IF NOT EXISTS Mesures (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    date_mesure DATE NOT NULL,
    valeur FLOAT NOT NULL,
    id_capteur INTEGER,
    FOREIGN KEY (id_capteur) REFERENCES Capteurs(id_capteur) ON DELETE CASCADE
);

-- Création de la table Facture pour stocker les factures liées aux maisons
CREATE TABLE IF NOT EXISTS Facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50) NOT NULL,
    date_facture DATE NOT NULL,
    montant FLOAT NOT NULL,
    id_maison INTEGER,
    FOREIGN KEY (id_maison) REFERENCES Maison(id_maison) ON DELETE CASCADE
);

-- Question 4 : Création d'un logement avec 4 pièces
INSERT INTO Maison (adresse, telephone, adresse_ip) VALUES ('123 Rue Exemple', '0102030405', '192.168.1.1');

-- Création des pièces de la maison
INSERT INTO Piece (nom, id_maison) VALUES ('Salon', 1);
INSERT INTO Piece (nom, id_maison) VALUES ('Cuisine', 1);
INSERT INTO Piece (nom, id_maison) VALUES ('Chambre', 1);
INSERT INTO Piece (nom, id_maison) VALUES ('Salle de Bain', 1);


-- Question 5 : Création de 4 types de capteurs/actionneurs
INSERT INTO Capteurs (type, port_com, reference, localisation, date_installation, id_piece) VALUES 
('Capteur de température', 'COM1', 'TEMP123', 'Salon', '2024-01-10', 1),
('Capteur de luminosité', 'COM2', 'LUM456', 'Cuisine', '2024-01-11', 2),
('consommation électrique', 'COM3', 'LUM456', 'chambre', '2024-01-11', 3),
('niveau d’eau', 'COM4', 'LUM456', 'salle de bain', '2024-01-11', 4);

-- Question 6 : Création de 2 capteurs/actionneurs
INSERT INTO Capteurs (type, port_com, reference, localisation, date_installation, id_piece) 
VALUES 
('Capteur de température', 'COM1', 'TEMP123', 'Salon', '2024-01-10', 1),
('Capteur de luminosité', 'COM2', 'LUM456', 'Cuisine', '2024-01-11', 2);

-- Question 7 : Création de 2 mesures par capteur/actionneur
INSERT INTO Mesures (date_mesure, valeur, id_capteur) VALUES 
('2024-01-15', 22.5, 1),
('2024-01-16', 23.0, 1),
('2024-01-15', 300.0, 2),
('2024-01-16', 320.0, 2);

-- Question 8 : Création de 4 factures
INSERT INTO Facture (type, date_facture, montant, id_maison) VALUES 
('Electricité', '2024-01-01', 100.50, 1),
('Eau', '2024-01-05', 30.25, 1),
('Gaz', '2024-01-10', 75.00, 1),
('Internet', '2024-01-15', 45.00, 1);