from fastapi import FastAPI, Request
from datetime import datetime
import sqlite3

app = FastAPI()

# Chemin de la base de données SQLite
DATABASE = "mesures.db"

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Mesures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_mesure TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Initialiser la base de données
init_db()

@app.post("/temperature")
async def recevoir_donnees(request: Request):
    """
    Route pour recevoir les données de l'ESP8266.
    """
    try:
        data = await request.json()  # Récupérer les données JSON envoyées par l'ESP
        temperature = data.get("temperature")
        humidity = data.get("humidity")

        if temperature is None or humidity is None:
            return {"status": "error", "message": "Données manquantes"}

        # Enregistrer les données dans la base de données
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        date_mesure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO Mesures (date_mesure, temperature, humidity) VALUES (?, ?, ?)",
            (date_mesure, temperature, humidity),
        )
        conn.commit()
        conn.close()

        # Afficher les données dans la console pour vérification
        print(f"Données reçues : Température = {temperature} °C, Humidité = {humidity} %")
        
        return {"status": "success", "message": "Données reçues et enregistrées"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/historique")
def historique():
    """
    Route pour afficher l'historique des mesures enregistrées.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM Mesures ORDER BY date_mesure DESC")
        mesures = c.fetchall()
        conn.close()

        historique = [
            {"id": row[0], "date_mesure": row[1], "temperature": row[2], "humidity": row[3]}
            for row in mesures
        ]

        return {"status": "success", "historique": historique}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)