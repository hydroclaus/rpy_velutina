import asyncio
import datetime
from pathlib import Path

# TCP server configuration
# die IP ADRESSE des Pico (des "Satelliten")
SERVER_IP = "192.168.178.58"
#SERVER_IP = "192.168.48.255"
SERVER_PORT = 8080
RECONNECT_DELAY_SECONDS = 3

now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
data_dir = Path(__file__).resolve().parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)
DATA_FILE = data_dir / f'sensor_data_{now}.csv'



with open(DATA_FILE, 'w') as fp:
        fp.write('datetime,DEVICE_ID,seconds_since_start,Temp [C],pres[hPa],relHum [%],gas[]\n')



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

                line = data.decode(errors='replace').strip()
                print(f"Received: {line}")
                with open(DATA_FILE, 'a') as fp:
                    fp.write(f'{datetime.datetime.now()}, {line}\n')

        except (ConnectionError, OSError, asyncio.TimeoutError) as err:
            print(f"Connection error: {err}")
        finally:
            if writer is not None:
                writer.close()
                await writer.wait_closed()

        print(f"Reconnecting in {RECONNECT_DELAY_SECONDS}s...")
        await asyncio.sleep(RECONNECT_DELAY_SECONDS)

# Run the client
asyncio.run(receive_temperature())
