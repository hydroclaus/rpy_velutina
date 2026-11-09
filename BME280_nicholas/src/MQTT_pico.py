import time
import network
from umqtt.simple import MQTTClient
from secrets import SSID, PASSWORD, SERVER_PORT

# MQTT-Broker IP (IP-Adresse deines zentralen Raspberry Pi)
MQTT_SERVER = '192.168.48.116'

CLIENT_ID = "pico_..."
TOPIC = b"haus/pico/.../temperatur"
KEEP_ALIVE = 60  # Keep-alive in Sekunden

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not SSID or SSID == 'your_ssid_here':
        raise RuntimeError('Missing Wi-Fi credentials. Set SSID and PASSWORD in the script.')

    print(f'Connecting to Wi-Fi SSID: {SSID}')

    while True:
        try:
            if not wlan.isconnected():
                wlan.connect(SSID, PASSWORD)

                # Wait up to 15 seconds for connection
                for _ in range(15):
                    if wlan.isconnected():
                        break
                    time.sleep(1)
                    print('.', end='')

            if wlan.isconnected():
                print()
                print('Connected to Wi-Fi')
                print('IP address:', wlan.ifconfig()[0])
                return wlan
                
        except Exception as e:
            print(f'\nWi-Fi connection error: {e}')

        print('\nRetrying Wi-Fi connection in 5 seconds...')
        time.sleep(5)
        
wlan = connect_wifi()

# MQTT Client initialisieren
client = MQTTClient(CLIENT_ID, MQTT_SERVER, KEEP_ALIVE)
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
        time.sleep(30)
except Exception as e:
    print("Fehler:", e)
    client.disconnect()