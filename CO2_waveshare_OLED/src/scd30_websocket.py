import asyncio
import datetime

# TCP server configuration
SERVER_IP = "192.168.178.82"
SERVER_PORT = 8080

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(f'../data/sensor_data_{now}.csv', 'w') as fp:
        fp.write('datetime,seconds_since_start,CO2 [PPM],Temp [C],relHum [%]\n')



async def receive_temperature():
    reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    try:
        while True:
            data = await reader.readline()
            if not data:
                print("Server closed connection")
                break
            print(f"Received: {data.decode().strip()}")
            with open(f'../data/sensor_data_{now}.csv', 'a') as fp:
                fp.write(f'{datetime.datetime.now()}, {data.decode().strip()}\n')
    finally:
        writer.close()
        await writer.wait_closed()

# Run the client
asyncio.run(receive_temperature())