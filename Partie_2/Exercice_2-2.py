from flask import Flask, render_template_string, request, jsonify
import sqlite3

app = Flask(__name__)

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

# Endpoint pour afficher un camembert des factures
@app.route('/factures/graph', methods=['GET'])
def chart_factures():
    try:
        # Récupérer les factures depuis la base de données
        conn = get_db_connection()
        factures = conn.execute('SELECT type, montant FROM Facture').fetchall()
        conn.close()

        # Préparer les données pour le graphique
        data = [["Type", "Montant"]]  # En-tête pour Google Charts
        data.extend([[facture["type"], facture["montant"]] for facture in factures])

        # Modèle HTML avec Google Charts
        chart_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Camembert des Factures</title>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {'packages':['corechart']});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart() {
                    var data = google.visualization.arrayToDataTable({{ data|tojson }});

                    var options = {
                        title: 'Répartition des Factures',
                        is3D: true
                    };

                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }
            </script>
        </head>
        <body>
            <h1>Répartition des Factures</h1>
            <div id="piechart" style="width: 900px; height: 500px;"></div>
        </body>
        </html>
        """

        # Générer la page HTML avec les données du graphique
        return render_template_string(chart_template, data=data)
    
    except Exception as e:
        return f"Erreur : {e}", 500

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)