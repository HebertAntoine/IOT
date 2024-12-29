from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import requests
from collections import defaultdict
from datetime import datetime
from datetime import datetime


app = Flask(__name__, static_folder='static', template_folder='templates')

# Clé API pour OpenWeatherMap
API_KEY = "623e5d8d1ee9b74bfa3dfb184717a49f"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
VILLE = "Paris,FR"

# python3 -m venv myenv
# source myenv/bin/activate
# pip install flask
# myenv\Scripts\activate
#

# connection a la database
def get_db_connection():
    conn = sqlite3.connect("logement.db")
    conn.row_factory = sqlite3.Row
    return conn

def format_date(date_str):
    """Format the date to display day and full date."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    day_name = date_obj.strftime("%A")
    full_date = date_obj.strftime("%d %B %Y")
    return day_name.capitalize(), full_date.capitalize()

# Route for index page
@app.route("/", endpoint="index")
def index():
    return render_template("index.html")


# Route for home page
@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")




# API to fetch all houses
@app.route("/api/houses")
def get_all_houses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_maison, adresse FROM Maison")
        houses = [{"id": row["id_maison"], "address": row["adresse"]} for row in cursor.fetchall()]
        conn.close()
        return jsonify({"houses": houses})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# House details with associated pieces
@app.route("/house/<int:house_id>")
def house_details(house_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch house details
        cursor.execute("SELECT adresse, telephone, adresse_ip FROM Maison WHERE id_maison = ?", (house_id,))
        house = cursor.fetchone()

        # Fetch pieces associated with the house
        cursor.execute("SELECT id_piece, nom FROM Piece WHERE id_maison = ?", (house_id,))
        pieces = cursor.fetchall()

        conn.close()

        if house:
            return render_template(
                "house_details.html",
                house_id=house_id,
                address=house["adresse"],
                phone=house["telephone"],
                ip_address=house["adresse_ip"],
                pieces=pieces
            )
        else:
            return "Maison introuvable.", 404
    except Exception as e:
        return f"Erreur : {str(e)}", 500

# Route pour afficher la page d'ajout d'une maison
@app.route("/add_house", methods=["GET", "POST"])
def add_house():
    if request.method == "POST":
        try:
            address = request.form.get("address")
            phone = request.form.get("phone")
            ip_address = request.form.get("ip_address")

            if address and phone and ip_address:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Maison (adresse, telephone, adresse_ip) VALUES (?, ?, ?)",
                               (address, phone, ip_address))
                conn.commit()
                conn.close()
                return redirect(url_for("home"))
            else:
                return "Tous les champs sont obligatoires.", 400
        except Exception as e:
            return f"Erreur : {str(e)}", 500
    return render_template("add_house.html")


# Route pour afficher la page de suppression d'une maison
@app.route("/delete_house", methods=["GET", "POST"])
def delete_house():
    if request.method == "POST":
        try:
            house_id = request.form.get("house_id")
            if house_id:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Maison WHERE id_maison = ?", (house_id,))
                conn.commit()
                conn.close()
                return redirect(url_for("home"))
            else:
                return "Aucune maison sélectionnée.", 400
        except Exception as e:
            return f"Erreur : {str(e)}", 500
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_maison, adresse FROM Maison")
        houses = cursor.fetchall()
        conn.close()
        return render_template("delete_house.html", houses=houses)


# Route pour afficher les capteurs d'une pièce
# Route pour afficher les détails d'une pièce et ses capteurs
@app.route("/piece/<int:piece_id>")
def piece_details(piece_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer les informations de la pièce et de la maison
        cursor.execute("SELECT nom, id_maison FROM Piece WHERE id_piece = ?", (piece_id,))
        piece = cursor.fetchone()

        if not piece:
            return "Pièce introuvable.", 404

        house_id = piece["id_maison"]

        # Récupérer les capteurs associés
        cursor.execute("""
            SELECT id_capteur, type, port_com, reference, localisation, date_installation, etat
            FROM Capteurs
            WHERE id_piece = ?
        """, (piece_id,))
        capteurs = cursor.fetchall()

        conn.close()

        # Passer house_id au template
        return render_template(
            "piece_details.html",
            piece_id=piece_id,
            house_id=house_id,
            piece_name=piece["nom"],
            capteurs=capteurs
        )
    except Exception as e:
        return f"Erreur : {str(e)}", 500



# Add a piece to a house
@app.route("/add_piece", methods=["GET"])
def add_piece_base():
    return "Veuillez spécifier un ID de maison dans l'URL.", 400
# Add a piece to a house
@app.route("/add_piece/<int:house_id>", methods=["POST"])
def add_piece(house_id):
    try:
        room_type = request.form.get("room_type")
        if not room_type:
            return "Le type de pièce est obligatoire.", 400

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Compter les pièces existantes du même type
        cursor.execute("""
            SELECT COUNT(*) FROM Piece
            WHERE id_maison = ? AND nom LIKE ?
        """, (house_id, f"{room_type}%"))
        count = cursor.fetchone()[0]

        # Générer le nom de la pièce avec un numéro incrémenté si nécessaire
        if count > 0:
            piece_name = f"{room_type} {count + 1}"
        else:
            piece_name = room_type

        # Ajouter la pièce à la base de données
        cursor.execute("""
            INSERT INTO Piece (nom, id_maison)
            VALUES (?, ?)
        """, (piece_name, house_id))
        conn.commit()
        conn.close()

        return redirect(url_for("house_details", house_id=house_id))
    except Exception as e:
        return f"Erreur lors de l'ajout de la pièce : {str(e)}", 500


# Delete a piece
@app.route("/delete_piece/<int:house_id>", methods=["GET", "POST"])
def delete_piece(house_id):
    if request.method == "POST":
        try:
            piece_id = request.form.get("piece_id")
            if piece_id:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Piece WHERE id_piece = ?", (piece_id,))
                conn.commit()
                conn.close()
                return redirect(url_for("house_details", house_id=house_id))
            else:
                return "Aucune pièce sélectionnée.", 400
        except Exception as e:
            return f"Erreur : {str(e)}", 500

    # Méthode GET : Charger les pièces disponibles pour cette maison
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_piece, nom FROM Piece WHERE id_maison = ?", (house_id,))
        pieces = cursor.fetchall()
        conn.close()

        # Rendre le template avec les pièces
        return render_template("delete_piece.html", house_id=house_id, pieces=pieces)
    except Exception as e:
        return f"Erreur lors du chargement des données : {str(e)}", 500

# Route pour afficher la page d'ajout d'un capteur
@app.route("/add_sensor/<int:piece_id>")
def add_sensor_page(piece_id):
    return render_template("add_sensor.html", piece_id=piece_id)


# Route pour ajouter un capteur
@app.route("/add_sensor/<int:piece_id>", methods=["GET", "POST"])
def add_sensor(piece_id):
    if request.method == "POST":
        try:
            date_installation = request.form.get("date_installation")
            localisation = request.form.get("localisation")
            reference = request.form.get("reference")
            sensor_type = request.form.get("type")
            port_com = request.form.get("port_com")

            if date_installation and localisation and reference and sensor_type and port_com:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Capteurs (id_piece, date_installation, localisation, reference, type, port_com)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (piece_id, date_installation, localisation, reference, sensor_type, port_com))
                conn.commit()
                conn.close()
                return redirect(url_for("piece_details", piece_id=piece_id))
            else:
                return "Tous les champs sont obligatoires.", 400
        except Exception as e:
            return f"Erreur lors de l'ajout : {str(e)}", 500

    return render_template("add_sensor.html", piece_id=piece_id)

# Route pour afficher les détails d'une pièce et ses capteurs
@app.route('/room/<int:piece_id>')
def room_details(piece_id):
    # Connexion à la base de données
    conn = sqlite3.connect('logement.db')
    cursor = conn.cursor()

    # Récupérer les capteurs associés à cette pièce
    cursor.execute("""
        SELECT id_capteur, type, port_com, reference, localisation, date_installation
        FROM Capteurs
        WHERE id_piece = ?
    """, (piece_id,))
    capteurs = cursor.fetchall()

    # Fermer la connexion
    conn.close()

    # Rendre le template avec les capteurs
    return render_template('room_details.html', capteurs=capteurs, piece_id=piece_id)

# Route pour afficher la page de suppression d'un capteur
@app.route("/delete_sensor/<int:piece_id>")
def delete_sensor_page(piece_id):
    try:
        conn = sqlite3.connect("logement.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id_capteur, reference FROM Capteurs WHERE id_piece = ?", (piece_id,))
        sensors = cursor.fetchall()
        conn.close()
        print(sensors)
        return render_template("delete_sensor.html", piece_id=piece_id, sensors=sensors)
    except Exception as e:
        return f"Erreur : {str(e)}", 500


# Route pour supprimer un capteur
@app.route("/delete_sensor", methods=["POST"])
def delete_sensor():
    try:
        sensor_id = request.form.get("sensor_id")
        piece_id = request.form.get("piece_id")

        if not sensor_id or not piece_id:
            return "Capteur ou pièce non spécifiée.", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Supprimer le capteur de la base de données
        cursor.execute("DELETE FROM Capteurs WHERE id_capteur = ?", (sensor_id,))
        conn.commit()
        conn.close()

        # Rediriger vers la page des détails de la pièce
        return redirect(url_for("piece_details", piece_id=piece_id))
    except Exception as e:
        return f"Erreur lors de la suppression : {str(e)}", 500

@app.route('/update_sensor_state/<int:id>', methods=['POST'])
def update_sensor_state(id):
    try:
        # Récupérer les données envoyées par le client
        data = request.get_json()
        etat = data['etat']  # 1 pour "Actif", 0 pour "Inactif"
        
        # Mettre à jour l'état du capteur dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Capteurs SET etat = ? WHERE id_capteur = ?", (etat, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "État du capteur mis à jour avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_db():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/sensor_graph/<int:sensor_id>', methods=['GET'])
def sensor_graph(sensor_id):
    # Récupérer les données du capteur et passer à un template pour afficher le graphique
    return render_template('graphique.html', sensor_id=sensor_id)
    
@app.route('/get_sensor_data/<int:sensor_id>', methods=['GET'])
def get_sensor_data(sensor_id):
    try:
        conn = sqlite3.connect('logement.db')
        cursor = conn.cursor()

        # Sélectionner les mesures du capteur donné
        cursor.execute('''
            SELECT date_mesure, valeur FROM Mesures WHERE id_capteur = ? ORDER BY date_mesure
        ''', (sensor_id,))
        data = cursor.fetchall()
        conn.close()

        # Formater les données pour le frontend
        measurements = [{'date_mesure': row[0], 'valeur': row[1]} for row in data]

        return jsonify(measurements)

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {str(e)}")
        return jsonify({"error": "Erreur lors de la récupération des données"}), 500


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

        # Vérifier que les données nécessaires sont présentes
        if 'temperature' in data and 'humidity' in data and 'id_capteur' in data:
            temperature = data['temperature']
            humidity = data['humidity']
            id_capteur = data['id_capteur']
            
            # Afficher la température et l'humidité reçues dans le terminal
            print(f"Température reçue : {temperature}°C, Humidité : {humidity}%, ID Capteur : {id_capteur}")
            
            # Insérer la température dans la base de données
            insert_measurement(temperature, id_capteur)
            
            # Répondre avec un message de succès
            return jsonify({"message": "Données reçues avec succès!"}), 200
        else:
            # Si les données sont manquantes
            return jsonify({"error": "Données manquantes"}), 400
    except Exception as e:
        # Afficher l'erreur si elle se produit
        print(f"Erreur : {str(e)}")
        return jsonify({"error": str(e)}), 500

# API pour récupérer les factures
@app.route("/factures/<int:house_id>")
def factures(house_id):
    try:
        print("Tentative de chargement du template factures.html...")
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer les factures liées à la maison
        cursor.execute("""
            SELECT id_facture, type, date_facture, montant 
            FROM Facture 
            WHERE id_maison = ?
        """, (house_id,))
        factures_raw = cursor.fetchall()
        conn.close()

        # Conversion des factures en dictionnaires
        factures = [
            {
                "id_facture": row["id_facture"],
                "type": row["type"],
                "date_facture": row["date_facture"],
                "montant": row["montant"],
            }
            for row in factures_raw
        ]

        print(f"Factures trouvées pour la maison {house_id} : {factures}")
        return render_template("factures.html", house_id=house_id, factures=factures)
    except Exception as e:
        print(f"Erreur lors de l'accès aux factures : {e}")
        return f"Erreur : {str(e)}", 500

# Route pour ajouter une facture
@app.route('/add_facture/<int:house_id>', methods=['POST'])
def add_facture(house_id):
    try:
        type_facture = request.form['type']
        date_facture = request.form['date_facture']
        montant = float(request.form['montant'])

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Facture (type, date_facture, montant, id_maison) VALUES (?, ?, ?, ?)',
            (type_facture, date_facture, montant, house_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('factures', house_id=house_id))
    except Exception as e:
        return f"Erreur lors de l'ajout de la facture : {e}"

@app.route('/delete_facture/<int:house_id>', methods=['POST'])
def delete_facture(house_id):
    try:
        # Récupérer l'ID de la facture à supprimer
        facture_id = request.form['id_facture']

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Supprimer la facture
        cursor.execute("DELETE FROM Facture WHERE id_facture = ?", (facture_id,))
        conn.commit()
        conn.close()

        # Rediriger vers la page des factures
        return redirect(url_for('factures', house_id=house_id))
    except Exception as e:
        return f"Erreur lors de la suppression de la facture : {e}", 500

@app.route('/get_factures_chart_data/<int:house_id>')
def get_factures_chart_data(house_id):
    scale = request.args.get('scale', 'month')  # Par défaut : mois
    facture_type = request.args.get('type', '').lower()  # Exemple : "water", "electricity", "gas"

    if facture_type not in ['water', 'electricity', 'gas']:
        return jsonify({'error': 'Type de facture invalide'}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date_facture, montant
                FROM Facture
                WHERE id_maison = ? AND LOWER(type) = ?
            """, (house_id, facture_type))
            factures = cursor.fetchall()

        # Transformer les données en liste Python
        factures = [{"date_facture": row["date_facture"], "montant": row["montant"]} for row in factures]

        # Agrégation selon l'échelle de temps
        if scale == 'day':
            labels, data_points = aggregate_by_day(factures)
        elif scale == 'month':
            labels, data_points = aggregate_by_month(factures)
        elif scale == 'year':
            labels, data_points = aggregate_by_year(factures)
        else:
            return jsonify({'error': 'Échelle de temps invalide'}), 400

        return jsonify({'labels': labels, 'data_points': data_points})

    except Exception as e:
        return jsonify({'error': f"Erreur lors de l'accès aux données : {e}"}), 500

def aggregate_by_day(factures):
    """Agrège les factures par jour."""
    aggregation = defaultdict(float)
    for facture in factures:
        date = facture["date_facture"]  # Format : YYYY-MM-DD
        aggregation[date] += facture["montant"]

    sorted_aggregation = sorted(aggregation.items())  # Tri par date
    labels = [item[0] for item in sorted_aggregation]
    data_points = [item[1] for item in sorted_aggregation]
    return labels, data_points

def aggregate_by_year(factures):
    """Agrège les factures par année."""
    aggregation = defaultdict(float)
    for facture in factures:
        date_obj = datetime.strptime(facture["date_facture"], "%Y-%m-%d")
        year = date_obj.strftime("%Y")  # Format : YYYY
        aggregation[year] += facture["montant"]

    sorted_aggregation = sorted(aggregation.items())  # Tri par date
    labels = [item[0] for item in sorted_aggregation]
    data_points = [item[1] for item in sorted_aggregation]
    return labels, data_points


def aggregate_by_month(factures):

    aggregation = defaultdict(float)
    for facture in factures:
        month = facture.date_facture.strftime('%Y-%m')  # Format YYYY-MM
        aggregation[month] += facture.montant

    sorted_aggregation = sorted(aggregation.items())  # Tri par date
    labels = [item[0] for item in sorted_aggregation]
    data_points = [item[1] for item in sorted_aggregation]
    return labels, data_points


# Route pour afficher la météo avec des icônes personnalisées
@app.route("/weather", methods=["GET"])
def weather():
    try:
        params = {
            "q": VILLE,
            "appid": API_KEY,
            "units": "metric",
            "cnt": 40,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        meteo_data = response.json()

        # Préparer les données météo
        previsions = []
        daily_data = {}

        # Associer les icônes personnalisées aux types de météo
        icon_mapping = {
            "clear": "clear.png",
            "rain": "rain.png",
            "clouds": "clouds.png",
            "snow": "snow.png",
            "thunderstorm": "thunderstorm.png",
        }

        # Grouper les prévisions par jour
        for forecast in meteo_data["list"]:
            date = forecast["dt_txt"].split(" ")[0]
            temperature = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"].lower()
            icon_key = next((key for key in icon_mapping if key in description), "clear")
            icon = icon_mapping.get(icon_key, "clear.png")

            if date not in daily_data:
                daily_data[date] = {
                    "temps": [],
                    "description": description,
                    "icon": icon,
                }
            daily_data[date]["temps"].append(temperature)

        # Résumer les données pour les 5 jours suivants
        for day, data in list(daily_data.items())[:5]:
            avg_temp = round(sum(data["temps"]) / len(data["temps"]), 2)
            day_name, full_date = format_date(day)
            previsions.append({
                "day_name": day_name,
                "full_date": full_date,
                "temperature": avg_temp,
                "description": data["description"],
                "icon": data["icon"],
            })

        # Rendre le modèle avec les prévisions météo
        return render_template("weather.html", ville=VILLE, previsions=previsions)

    except requests.exceptions.RequestException as e:
        return f"<h1>Erreur : {str(e)}</h1>", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
