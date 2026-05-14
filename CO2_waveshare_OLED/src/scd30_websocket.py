import asyncio

# TCP server configuration
SERVER_IP = "192.168.178.82"
SERVER_PORT = 8080

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
    finally:
        writer.close()
        await writer.wait_closed()

# Run the client
asyncio.run(receive_temperature())