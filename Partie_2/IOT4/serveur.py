from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Fonction pour insérer une mesure dans la table Mesures
def insert_measurement(valeur, id_capteur):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('logement.db')
    c = conn.cursor()

    # Obtenez la date et l'heure actuelles
    date_mesure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insertion de la mesure dans la table Mesures
    c.execute('''
        INSERT INTO Mesures (date_mesure, valeur, id_capteur)
        VALUES (?, ?, ?)
    ''', (date_mesure, valeur, id_capteur))

    conn.commit()
    conn.close()

# Route pour recevoir les données de température et d'humidité
@app.route('/temperature', methods=['POST'])
def handle_temperature():
    try:
        # Récupérer les données envoyées par l'ESP8266 ou curl
        data = request.get_json()

        # Afficher les données reçues pour le débogage
        print(f"Données reçues : {data}")

        if 'temperature' in data and 'humidity' in data and 'id_capteur' in data:
            temperature = data['temperature']
            humidity = data['humidity']
            id_capteur = data['id_capteur']
            
            # Afficher la température et l'humidité reçues dans le terminal
            print(f"Température reçue : {temperature}°C, Humidité : {humidity}%, ID Capteur : {id_capteur}")
            
            # Insérer la température dans la base de données
            insert_measurement(temperature, id_capteur)
            
            # Insérer l'humidité dans la base de données (si nécessaire)
            insert_measurement(humidity, id_capteur)
            
            # Répondre avec un message de succès
            return jsonify({"message": "Données reçues avec succès!"}), 200
        else:
            # Si les données sont manquantes
            return jsonify({"error": "Données manquantes"}), 400
    except Exception as e:
        # Afficher l'erreur si elle se produit
        print(f"Erreur : {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Démarre le serveur Flask en écoutant sur toutes les interfaces réseau
    app.run(host='0.0.0.0', port=5000, debug=True)