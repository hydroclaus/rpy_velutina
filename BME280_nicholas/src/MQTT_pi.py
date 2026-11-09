import paho.mqtt.client as mqtt

KEEP_ALIVE = 60  # Keep-alive in Sekunden

# Empfangs-Funktion
def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode()} °C")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbunden mit MQTT-Broker")
        client.subscribe("haus/pico/+/temperatur") # "+" --> alle Picos werden abgefragt/abonniert
        print("Abonniert: haus/pico/+/temperatur")
        print("Listening...")
    else:
        print(f"Verbindungsfehler: {rc}")

# Client starten und verbinden
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_message = on_message # client.on_message definieren mit on_message. Aufruf der Funktion passiert im Hintergrund automatisch
client.on_connect = on_connect
client.connect("localhost", 1883, KEEP_ALIVE)

# Endlosschleife zum Lauschen
client.loop_forever()