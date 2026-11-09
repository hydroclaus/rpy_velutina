import time
import network
from umqtt.simple import MQTTClient

# WLAN-Zugangsdaten
WLAN_SSID = "Dein_WLAN_Name"
WLAN_PASS = "Dein_WLAN_Passwort"

# MQTT-Broker IP (IP-Adresse deines zentralen Raspberry Pi)
MQTT_SERVER = "192.168.1.100"
CLIENT_ID = "pico_wohnzimmer"
TOPIC = b"haus/pico/wohnzimmer/temperatur"

# WLAN verbinden
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WLAN_SSID, WLAN_PASS)
while not wlan.isconnected():
    time.sleep(1)
print("WLAN verbunden!")

# MQTT Client initialisieren
client = MQTTClient(CLIENT_ID, MQTT_SERVER)
client.connect()

try:
    while True:
        # Hiertemperatur messen (Beispielwert, ersetze dies durch deinen Sensor-Code)
        temperatur = 21.5 
        
        # Daten senden
        payload = str(temperatur)
        client.publish(TOPIC, payload)
        print(f"Gesendet: {payload}°C")
        
        # Alle 60 Sekunden wiederholen
        time.sleep(60)
except Exception as e:
    print("Fehler:", e)
    client.disconnect()