####################################################################################################################################################
#                                                                                                                                                  #
#                                                 Partie 1                                                                                         #
#                                                                                                                                                  #
####################################################################################################################################################



Dans le fichier Partie_1 il y a tout ce qui concernet la Base de données question de 1 à 8 dans logement.sql et la 1.2 dans remplissage.py

la Question 2 entre les lignes 1-8
- Suppression des tables existantes avec DROP TABLE IF EXISTS { nom de la table }

la Question 3 entre les lignes 11-64
- CREATE TABLE IF NOT EXISTS { nom de la table }

la Question 4 entre les lignes 65-74
- Création d'un logement avec 4 pièces avec la ligne INSERT INTO { nom de la table } VALUES ({ les valeurs a la suite des colones })

la Question 5 entre les lignes 75-81
- Création de 4 types de capteurs/actionneurs avec la ligne INSERT INTO { nom de la table } VALUES ({ les valeurs a la suite des colones })

la Question 6 entre les lignes 82-87
- Création de 2 capteurs/actionneurs avec la ligne INSERT INTO { nom de la table } VALUES ({ les valeurs a la suite des colones })

la Question 7 entre les lignes 88-94
- Création de 2 mesures par capteur/actionneur avec la ligne INSERT INTO { nom de la table } VALUES ({ les valeurs a la suite des colones })

la Question 8 entre les lignes 95-100
- Création de 4 factures avec la ligne INSERT INTO { nom de la table } VALUES ({ les valeurs a la suite des colones })

Dans le fichier remplissage.py il y a l'exercice 1.2
le programme va ce connecter a la base de données, puis on va exectuter les ligne SQL du fichier logement.sql pour preparer la base de données
puis il va definir les valeurs des mesures et les inserts dans la base de données et la meme choses pour les factures




####################################################################################################################################################
#                                                                                                                                                  #
#                                                 Partie 2                                                                                         #
#                                                                                                                                                  #
####################################################################################################################################################





Toute la partie 2 Serveur RESTful est dans le fichier Partie_2

Exercice 2.1 : permet de récupérer et ajouter des données de mesures et de factures depuis une base de données SQLite en utilisant des requêtes GET et POST

Exercice 2.2 : on peut voir directement le graphique dans la page web : http://127.0.0.1:5000/factures/graph

Exercice 2.3 : Dans cette exercice il y a l'exercice 1 et 2 que 'lon peut voir directement dans les different liens suivant : 

- http://127.0.0.1:8000/factures/chart
- http://127.0.0.1:8000/meteo
- http://127.0.0.1:8000/mesures

Exercice 2.4 : 

Il faut placer le SSID et password dans les 2 lignes suivante : // Paramètres Wi-Fi
const char* ssid = 
const char* password = 

et a la ligne : const char* serverName = il faut mettre l'IP du serveur qui sera donnée au moment ou le serveur sera demarré

Ce code permet à un ESP8266 de se connecter à un réseau Wi-Fi, de lire les données de température et d’humidité à l’aide d’un capteur DHT11, puis d’envoyer ces données sous forme de requête POST en JSON à un serveur Python local via HTTP toutes les 60 secondes. 
Il utilise la bibliothèque ESP8266WiFi pour la connexion Wi-Fi et ESP8266HTTPClient pour envoyer les données.





####################################################################################################################################################
#                                                                                                                                                  #
#                                                 Partie 3                                                                                         #
#                                                                                                                                                  #
####################################################################################################################################################






Il faut placer le SSID et password dans les 2 lignes suivante : // Paramètres Wi-Fi
const char* ssid = 
const char* password = 

et a la ligne : const char* serverName = il faut mettre l'IP du serveur qui sera donnée au moment ou le serveur sera demarré

Ce programme permet de gérer des maisons et leurs composants dans une base de données SQLite. Il permet d’afficher et manipuler les maisons (ajout, suppression, détails) ainsi que leurs pièces et capteurs associés via des routes API. 
De plus, il affiche des prévisions météo à partir de l’API OpenWeatherMap et permet de visualiser les factures liées à chaque maison sous forme graphique. 
Il comprend aussi des routes pour l’ajout et la suppression de capteurs et de pièces dans une maison.
Le programme interagie bien avec la base de données et il est capable aussi de mettre a jour les données recu par l'esp pour les afficher sur le graphique du capteur
dans tempates il y a toutes les pages
dans static il y a toute les images ou icones

Partie_3
-- static
-- templates
-- -- index.html
-- -- weather.html
-- -- home.html
-- -- house_details.html
-- -- piece_details.html
-- -- graphique.html
-- -- factures.html
-- logement.db
-- logement.sql
-- Site.py
