import paho.mqtt.client as mqtt

# Empfangs-Funktion
def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode()} °C")

# Client starten und verbinden
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_message = on_message # client.on_message definieren mit on_message. Aufruf der Funktion passiert im Hintergrund automatisch
client.connect("localhost", 1883)
client.subscribe("haus/pico/+/temperatur")

# Endlosschleife zum Lauschen
client.loop_forever()