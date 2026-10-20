import asyncio
import datetime
from pathlib import Path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# TCP server configuration
# die IP ADRESSE des Pico (des "Satelliten")
# SERVER_IP = "192.168.48.246"
SERVER_IPS = ["192.168.179.8", "192.168.179.9"] # ['192.168.48.148', '192.168.48.158', '192.168.48.246', '192.168.48.156', '192.168.48.27', '192.168.48.133', '192.168.48.192', '192.168.48.118']
SERVER_PORT = 8080
RECONNECT_DELAY_SECONDS = 3

# InfluxDB connection settings
INFLUX_URL = "http://localhost:8086/"
INFLUX_TOKEN = "6F3dp83e2vfwPQS42VvwPyK0PLn2d1alyq3suEE4M_Bt116HaFfquTVCMGCe8BcH8k4YCb0kb1RMjyau0t5hDA=="
INFLUX_ORG = "vegas"
INFLUX_BUCKET = "TechnikumTP"

# Create InfluxDB client (establish connection)
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
# Create a write API, for sending data to InfluxDB (Synchronous --> wait for confirmation of write)
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Create file for storing data on local drive
now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
data_dir = Path(__file__).resolve().parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)
DATA_FILE = data_dir / f'sensor_data_{now}.csv'



# Write header to DATA_FILE
with open(DATA_FILE, 'w') as fp:
    fp.write('datetime,DEVICE_ID,seconds_since_start,Temp [C],pres [hPa]\n')


def write_to_influx(line: str) -> None:
    # line format: DEVICE_ID,seconds_since_start,Temp [C],pres [hPa]
    fields = [part.strip() for part in line.split(',')]
    device_id, seconds_since_start, temp_c, pres_hpa = fields
    # Create ("measurement") Point for sending and writing to db
    point = (
        Point(INFLUX_BUCKET)
        .tag("DEVICE_ID", device_id)
        .field("seconds_since_start", float(seconds_since_start))
        .field("temp_c", float(temp_c))
        .field("pres_hpa", float(pres_hpa))
    )
    # send (data) Point
    influx_write_api.write(bucket=INFLUX_BUCKET, record=point)


async def receive_temperature(ip: str):
    while True:
        writer = None
        try:
            # Establish async. network connection to server with "network address" and specific "door", without freezing the program while waiting
            reader, writer = await asyncio.open_connection(ip, SERVER_PORT)
            # reader --> tool for reading, writer --> tool for writing
            print(f"Connected to {ip}:{SERVER_PORT}")

            while True:
                # Read the data until break line point (\n)
                data = await reader.readline()
                if not data:
                    print("Server closed connection")
                    break
                now = datetime.datetime.now()

                # decode bytes from data to line
                line = data.decode(errors='replace').strip()
                print(f"Received @ {now.strftime('%Y-%m-%d %H:%M:%S')}: {line}")

                # Write data (line) to DATA_FILE
                with open(DATA_FILE, 'a') as fp:
                    fp.write(f'{now},{line}\n')
                # Send data to db
                try:
                    print("Trying to write data to InfluxDB...")
                    write_to_influx(line)
                    print("Data written to InfluxDB")
                except (ValueError, ConnectionError, OSError) as err:
                    print(f"InfluxDB write error: {err}")

        except (ConnectionError, OSError, asyncio.TimeoutError) as err:
            print(f"Connection error: {err}")
        finally:
            if writer is not None:
                # Close network connection (port)
                writer.close()
                # Wait for completion of writer.close()
                await writer.wait_closed()

        print(f"Reconnecting in {RECONNECT_DELAY_SECONDS}s...")
        await asyncio.sleep(RECONNECT_DELAY_SECONDS)

async def main():
    # Erstellt für jede IP in der Liste einen eigenen parallelen Task
    tasks = [receive_temperature(ip) for ip in SERVER_IPS]
    # Führt alle Tasks gleichzeitig im selben Event-Loop aus
    await asyncio.gather(*tasks) # * zum entpacken der Liste in einzelne Argumente für gather

# Run the client
# if __name__ == "__main__":
try:
    asyncio.run(main())
finally:
    influx_write_api.close()
    influx_client.close()
