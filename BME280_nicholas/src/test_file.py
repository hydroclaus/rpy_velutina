import machine
import utime

led = machine.Pin("LED", machine.Pin.OUT)
while True:
    led.toggle()
    utime.sleep(0.5)


            ### pi
            verify = False
            while verify is False:
                if writer is not None:
                    writer.close()
                    await writer.wait_closed()
                reader, writer = await asyncio.open_connection(ip, SERVER_PORT)
                print(f"Connected to {ip}:{SERVER_PORT}")

                # verfication, check if connected to Pico
                print("Verify...")
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=3.0)
                    verification = data.decode(errors='replace').strip()
                except:
                    verification = "Not verified"
                if verification == "I'm a Pico":
                    print("Verification complete")
                    print()
                    verify = True
                else:
                    print("Not verified...")


            ### pico
            # Send verification if client is connected 
            print("Send verification...")
            line = "I'm a Pico\n"
            client.send(line.encode('utf-8'))