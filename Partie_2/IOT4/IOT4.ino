#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// Paramètres Wi-Fi
// const char* ssid = "Livebox-FBC0";  // Remplacez par votre SSID Wi-Fi
// const char* password = "7jJNoG66nKAfoUzn4E";   // Remplacez par votre mot de passe Wi-Fi


const char* ssid = "Iphone";  // Remplacez par votre SSID Wi-Fi
const char* password = "bbbbbbbb";   // Remplacez par votre mot de passe Wi-Fi

// Paramètres du capteur DHT
#define DHTPIN 0               // Pin où le DHT est connecté
#define DHTTYPE DHT11          // DHT 11 ou DHT 22
DHT dht(DHTPIN, DHTTYPE);

// URL du serveur Python
const char* serverName = "http://172.20.10.7:5000/temperature";  // Remplacez par l'IP de votre serveur Python

WiFiClient wifiClient;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connexion au réseau Wi-Fi
  Serial.println("Connexion au Wi-Fi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.print("IP : ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Attendre 60 secondes entre chaque lecture
  delay(60000);

  // Lire la température et l'humidité
  float t = dht.readTemperature();  // Température en °C
  float h = dht.readHumidity();    // Humidité en %

  // Vérifier si les lectures ont échoué
  if (isnan(t) || isnan(h)) {
    Serial.println(F("Erreur de lecture du capteur DHT!"));
    return;
  }

  // Créer les données JSON à envoyer avec l'ID du capteur
  String postData = "{\"temperature\": " + String(t) + ", \"humidity\": " + String(h) + ", \"id_capteur\": 1}";

  // Afficher les données envoyées dans le moniteur série
  Serial.println("Envoi des données : " + postData);

  // Envoyer les données au serveur Python
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(wifiClient, serverName);  // Utiliser wifiClient ici
    http.addHeader("Content-Type", "application/json");

    // Envoyer une requête POST avec les données
    int httpResponseCode = http.POST(postData);

    // Vérifier la réponse du serveur
    Serial.print("Code réponse HTTP : ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : ");
      Serial.println(response);
    } else {
      Serial.print("Erreur de requête HTTP : ");
      Serial.println(httpResponseCode);
    }

    // Fermer la connexion HTTP
    http.end();
  } else {
    Serial.println("Erreur de connexion Wi-Fi");
  }
}
