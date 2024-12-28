from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from jinja2 import Template
import sqlite3

# Création de l'application FastAPI

# http://127.0.0.1:8000/factures/chart
# http://127.0.0.1:8000/meteo
# http://127.0.0.1:8000/mesures


app = FastAPI()

# Clé API pour OpenWeatherMap
API_KEY = "623e5d8d1ee9b74bfa3dfb184717a49f"  # Remplacez par votre clé API
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
VILLE = "Paris,FR"  # Paris comme ville fixe

# Fonction pour établir une connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API météo et factures !"}

# Route GET pour récupérer toutes les mesures
@app.get("/mesures")
async def get_mesures():
    conn = get_db_connection()
    mesures = conn.execute('SELECT * FROM Mesures').fetchall()
    conn.close()

    mesures_list = []
    for mesure in mesures:
        mesures_list.append({
            'id_mesure': mesure['id_mesure'],
            'date_mesure': mesure['date_mesure'],
            'valeur': mesure['valeur'],
            'id_capteur': mesure['id_capteur']
        })

    return {"mesures": mesures_list}

# Route pour afficher les prévisions météorologiques pour Paris
@app.get("/meteo", response_class=HTMLResponse)
async def meteo_5_jours():
    try:
        # Construire l'URL de l'API avec les paramètres pour Paris
        params = {
            "q": VILLE,
            "appid": API_KEY,
            "units": "metric",  # Températures en Celsius
            "cnt": 40,          # Nombre d'entrées horaires (8 par jour pour 5 jours)
        }
        # Faire la requête à l'API météo
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Vérifier si la requête est correcte
        meteo_data = response.json()

        # Préparer les données pour l'affichage et des actions éco-responsables
        previsions = []
        actions = []

        # Regrouper les prévisions par jour et calculer la température moyenne
        day_temps = {}
        for forecast in meteo_data["list"]:
            date = forecast["dt_txt"]
            day = date.split(" ")[0]  # Extraire la date (jour)

            temperature = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]

            if day not in day_temps:
                day_temps[day] = {"temps": [], "description": description}
            day_temps[day]["temps"].append(temperature)

        # Calculer la température moyenne pour chaque jour
        for day, data in day_temps.items():
            avg_temp = round(sum(data["temps"]) / len(data["temps"]), 2)  # Moyenne des températures horaires
            previsions.append({
                "date": day,
                "temperature": avg_temp,
                "description": data["description"]
            })

            # Déterminer l'action éco-responsable à partir de la météo
            if "rain" in data["description"].lower():
                actions.append(f"Le {day}: Il pleut, pas besoin d'arroser le jardin.")
            elif "clear" in data["description"].lower():
                actions.append(f"Le {day}: Il fait ensoleillé, c'est une bonne journée pour allumer le panneau solaire!")
            elif avg_temp > 25:
                actions.append(f"Le {day}: Il fait chaud, pensez à arroser les plantes et à prendre soin du jardin.")
            elif avg_temp < 10:
                actions.append(f"Le {day}: Il fait froid, pensez à protéger vos plantes du gel.")
            else:
                actions.append(f"Le {day}: Météo modérée, gardez un œil sur les conditions avant de prendre des mesures éco-responsables.")

        meteo_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prévisions Météo et Actions Éco-Responsables</title>
        </head>
        <body>
            <h1>Prévisions Météo pour {{ ville }}</h1>
            <ul>
                {% for prev in previsions %}
                <li>
                    <strong>{{ prev.date }}</strong>: {{ prev.temperature }}°C, {{ prev.description }}
                </li>
                {% endfor %}
            </ul>

            <h2>Recommandations Éco-Responsables :</h2>
            <ul>
                {% for action in actions %}
                <li>{{ action }}</li>
                {% endfor %}
            </ul>
        </body>
        </html>
        """
        template = Template(meteo_template)
        return HTMLResponse(content=template.render(ville=VILLE, previsions=previsions, actions=actions), status_code=200)

    except requests.exceptions.RequestException as e:
        return HTMLResponse(content=f"<h1>Erreur lors de la récupération des données météo : {str(e)}</h1>", status_code=500)

# Route pour afficher un graphique de type camembert des factures
@app.get("/factures/chart", response_class=HTMLResponse)
async def chart_factures():
    try:
        # Récupérer les factures depuis la base de données
        conn = get_db_connection()
        factures = conn.execute('SELECT type, montant FROM Facture').fetchall()
        conn.close()

        # Préparer les données pour Google Charts
        data = [["Type", "Montant"]]  # En-tête pour Google Charts
        data.extend([[facture["type"], facture["montant"]] for facture in factures])

        # Modèle HTML pour le graphique Google Chart
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
        template = Template(chart_template)
        return HTMLResponse(content=template.render(data=data))
    
    except Exception as e:
        return f"Erreur : {e}", 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)