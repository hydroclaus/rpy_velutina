import paho.mqtt.client as mqtt
import datetime
from pathlib import Path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection settings
INFLUX_URL = "http://localhost:8086/"
INFLUX_TOKEN = "6F3dp83e2vfwPQS42VvwPyK0PLn2d1alyq3suEE4M_Bt116HaFfquTVCMGCe8BcH8k4YCb0kb1RMjyau0t5hDA=="
INFLUX_ORG = "vegas"
INFLUX_BUCKET = "TechnikumTP"

TOPIC = "vegas/+/temperatur" # client.subscribe("vegas/+/temperatur") # "+" --> alle Picos werden abgefragt/abonniert. Wenn nur einer, dann vegas/name_pico/temperatur
KEEP_ALIVE = 60  # Keep-alive in Sekunden

def write_to_influx(line: str) -> None:
    # line format: DEVICE_ID,seconds_since_start,Temp [C],pres [hPa], relHum [%]
    fields = [part.strip() for part in line.split(',')]
    device_id, seconds_since_start, temp_c, pres_hpa, rel_hum = fields
    # Create ("measurement") Point for sending and writing to db
    point = (
        Point(INFLUX_BUCKET)
        .tag("DEVICE_ID", device_id)
        .field("seconds_since_start", float(seconds_since_start))
        .field("temp_c", float(temp_c))
        .field("pres_hpa", float(pres_hpa))
        .field("rel_hum", float(rel_hum))
    )
    # send (data) Point
    influx_write_api.write(bucket=INFLUX_BUCKET, record=point)

# Empfangs-Funktion
def on_message(client, userdata, msg):
    line = msg.payload.decode()
    print(f"Empfangen: {line} -> {msg.topic}")

    with open(DATA_FILE, 'a') as fp:
        fp.write(f'{now},{line}\n')

    try:
        print("Trying to write data to InfluxDB...")
        write_to_influx(line)
        print("Data written to InfluxDB")
    except (ValueError, ConnectionError, OSError) as err:
        print(f"InfluxDB write error: {err}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbunden mit MQTT-Broker")
        client.subscribe(TOPIC)
        print("Abonniert: " + TOPIC)
        print("Warten auf Daten...")
    else:
        print(f"Verbindungsfehler: {rc}")

# Create InfluxDB client (establish connection)
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
# Create a write API, for sending data to InfluxDB (Synchronous --> wait for confirmation of write)
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Create file for storing data on local drive
now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
data_dir = Path(__file__).resolve().parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)
# DATA_FILE = data_dir / f'sensor_data_{now}.csv'
DATA_FILE = "/home/claus/Repository/rpy_velutina/BME280_nicholas/src/data/" + f'sensor_data_{now}.csv'

# Write header to DATA_FILE
with open(DATA_FILE, 'w') as fp:
    fp.write('datetime,DEVICE_ID,seconds_since_start,Temp [C],pres [hPa], relHum [%]\n')

# Client starten und verbinden
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_message = on_message # client.on_message definieren mit on_message. Aufruf der Funktion passiert im Hintergrund automatisch.
client.on_connect = on_connect
client.connect("localhost", 1883, keepalive=KEEP_ALIVE) # localhost statt ip, da listening skript auf dem raspberry laeuft, auf dem auch der mqtt-broker installiert ist

try:
    # Endlosschleife zum Lauschen
    client.loop_forever()
finally:
    influx_write_api.close()
    influx_client.close()