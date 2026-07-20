import asyncio
import datetime

# TCP server configuration
SERVER_IP = "192.168.178.82"
SERVER_PORT = 8080
RECONNECT_DELAY_SECONDS = 3

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
DATA_FILE = f'../data/sensor_data_{now}.csv'



with open(DATA_FILE, 'w') as fp:
        fp.write('datetime,seconds_since_start,CO2 [PPM],Temp [C],relHum [%]\n')



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