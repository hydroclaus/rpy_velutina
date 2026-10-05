import asyncio
import datetime
from pathlib import Path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# TCP server configuration
# die IP ADRESSE des Pico (des "Satelliten")
SERVER_IP = "192.168.178.58"
#SERVER_IP = "192.168.48.255"
SERVER_PORT = 8080
RECONNECT_DELAY_SECONDS = 3

# InfluxDB connection settings
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "VRXxOsHsqnucFSelWqcIxSUNO4GLMJHlI5btrPn8Efz5GDNw3k1dNOxiXbd9WCQaBv2b5Vky5DBAhP2EHpL-kg=="
INFLUX_ORG = "CPH"
INFLUX_BUCKET = "SensorsAmadeus34"

influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)

now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
data_dir = Path(__file__).resolve().parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)
DATA_FILE = data_dir / f'sensor_data_{now}.csv'



with open(DATA_FILE, 'w') as fp:
        fp.write('datetime,DEVICE_ID,seconds_since_start,Temp [C],pres[hPa],relHum [%],gas[]\n')


def write_to_influx(line: str) -> None:
    # line format: DEVICE_ID,seconds_since_start,Temp [C],pres[hPa],relHum [%],gas[]
    fields = [part.strip() for part in line.split(',')]
    device_id, seconds_since_start, temp_c, pres_hpa, rel_hum, gas = fields
    point = (
        Point(INFLUX_BUCKET)
        .tag("DEVICE_ID", device_id)
        .field("seconds_since_start", float(seconds_since_start))
        .field("temp_c", float(temp_c))
        .field("pres_hpa", float(pres_hpa))
        .field("rel_hum", float(rel_hum))
        .field("gas", float(gas))
    )
    influx_write_api.write(bucket=INFLUX_BUCKET, record=point)



async def receive_temperature():
    while True:
        writer = None
        try:
            reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
            print(f"Connected to {SERVER_IP}:{SERVER_PORT}")

            while True:
                data = await reader.readline()
                if not data:
                    print("Server closed connection")
                    break
                now = datetime.datetime.now()

                line = data.decode(errors='replace').strip()
                print(f"Received @ {now.strftime('%Y-%m-%d %H:%M:%S')}: {line}")
                with open(DATA_FILE, 'a') as fp:
                    fp.write(f'{now}, {line}\n')
                try:
                    write_to_influx(line)
                except (ValueError, ConnectionError, OSError) as err:
                    print(f"InfluxDB write error: {err}")

        except (ConnectionError, OSError, asyncio.TimeoutError) as err:
            print(f"Connection error: {err}")
        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()

        print(f"Reconnecting in {RECONNECT_DELAY_SECONDS}s...")
        await asyncio.sleep(RECONNECT_DELAY_SECONDS)

# Run the client
try:
    asyncio.run(receive_temperature())
finally:
    influx_write_api.close()
    influx_client.close()
