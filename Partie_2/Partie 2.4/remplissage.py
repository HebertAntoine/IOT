from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime

app = FastAPI()

DATABASE = "bibli.db"

# Connexion à la base de données (création des tables si nécessaires)
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Mesures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_mesure TEXT NOT NULL,
        valeur REAL NOT NULL,
        id_capteur INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route pour recevoir les données de l'ESP8266
@app.post("/envoyer-donnees")
async def recevoir_donnees(request: Request):
    data = await request.json()  # Lire les données JSON envoyées par l'ESP8266
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    # Insérer les données dans la base de données
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    date_mesure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO Mesures (date_mesure, valeur, id_capteur) VALUES (?, ?, ?)",
        (date_mesure, temperature, 1)  # ID du capteur = 1 (par exemple)
    )
    conn.commit()
    conn.close()

    # Définir une température seuil pour allumer une LED
    TEMPERATURE_SEUIL = 25.0  # Exemple : 25°C
    action_led = "ON" if temperature > TEMPERATURE_SEUIL else "OFF"

    # Retourner la réponse à l'ESP8266
    return {"message": "Données reçues avec succès", "action_led": action_led}