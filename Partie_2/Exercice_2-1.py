from flask import Flask, render_template_string, request, jsonify 
import sqlite3

app = Flask(__name__)


###
#
#   ce programme va cree un graphyque dynamique concernant toute les energies consommé via les factures dans la base de donnée
#   ce graphique est un camenber que on peut retrouver sur ce liens : 
#   http://127.0.0.1:5000/mesures
#   http://127.0.0.1:5000/factures
#   
#   GET http://127.0.0.1:5000/mesures
#   GET http://127.0.0.1:5000/factures
#   POST http://127.0.0.1:5000/mesures
#   POST http://127.0.0.1:5000/factures
#   
#   
###

# Fonction pour établir une connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route GET pour récupérer toutes les mesures
@app.route('/mesures', methods=['GET'])
def get_mesures():
    conn = get_db_connection()
    mesures = conn.execute('SELECT * FROM Mesures').fetchall()
    conn.close()

    # Convertir les résultats en format JSON
    mesures_list = []
    for mesure in mesures:
        mesures_list.append({
            'id_mesure': mesure['id_mesure'],
            'date_mesure': mesure['date_mesure'],
            'valeur': mesure['valeur'],
            'id_capteur': mesure['id_capteur']
        })

    return jsonify(mesures_list)


# Route GET pour récupérer toutes les factures
@app.route('/factures', methods=['GET'])
def get_factures():
    conn = get_db_connection()
    factures = conn.execute('SELECT * FROM Facture').fetchall()
    conn.close()

    # Convertir les résultats en format JSON
    factures_list = []
    for facture in factures:
        factures_list.append({
            'id_facture': facture['id_facture'],
            'type': facture['type'],
            'date_facture': facture['date_facture'],
            'montant': facture['montant'],
            'id_maison': facture['id_maison']
        })

    return jsonify(factures_list)

# Route POST pour ajouter une nouvelle mesure
@app.route('/mesures', methods=['POST'])
def add_mesure():
    data = request.get_json()

    # Extraire les données envoyées par le client
    date_mesure = data['date_mesure']
    valeur = data['valeur']
    id_capteur = data['id_capteur']

    # Insertion des données dans la base de données
    conn = get_db_connection()
    conn.execute('INSERT INTO Mesures (date_mesure, valeur, id_capteur) VALUES (?, ?, ?)',
                 (date_mesure, valeur, id_capteur))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Mesure ajoutée avec succès'}), 201

# Route POST pour ajouter une nouvelle facture
@app.route('/factures', methods=['POST'])
def add_facture():
    data = request.get_json()

    # Extraire les données envoyées par le client
    type_facture = data['type']
    date_facture = data['date_facture']
    montant = data['montant']
    id_maison = data['id_maison']

    # Insertion des données dans la base de données
    conn = get_db_connection()
    conn.execute('INSERT INTO Facture (type, date_facture, montant, id_maison) VALUES (?, ?, ?, ?)',
                 (type_facture, date_facture, montant, id_maison))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Facture ajoutée avec succès'}), 201

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)