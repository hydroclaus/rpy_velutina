import paho.mqtt.client as mqtt

TOPIC = "vegas/+/temperatur" # client.subscribe("vegas/+/temperatur") # "+" --> alle Picos werden abgefragt/abonniert. Wenn nur einer, dann vegas/name_pico/temperatur
KEEP_ALIVE = 60  # Keep-alive in Sekunden

# Empfangs-Funktion
def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode()}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbunden mit MQTT-Broker")
        client.subscribe(TOPIC)
        print("Abonniert: " + TOPIC)
        print("Warten auf Daten...")
    else:
        print(f"Verbindungsfehler: {rc}")

# Client starten und verbinden
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_message = on_message # client.on_message definieren mit on_message. Aufruf der Funktion passiert im Hintergrund automatisch.
client.on_connect = on_connect
client.connect("localhost", 1883, keepalive=KEEP_ALIVE) # localhost statt ip, da listening skript auf dem raspberry laeuft, auf dem auch der mqtt-broker installiert ist

# Endlosschleife zum Lauschen
client.loop_forever()