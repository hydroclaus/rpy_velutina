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

#################################################################################################################

import time
from rich.live import Live
from rich.table import Table

def generate_display(i):
    table = Table(title="Live Status")

    table.add_column("Parameter")
    table.add_column("Wert")

    table.add_row("Status", "Running")
    table.add_row("Fortschritt", f"{i}%")
    table.add_row("Durchlauf", f"{i}/100")

    return table


with Live(
    generate_display(0),
    refresh_per_second=10,
    transient=False
) as live:

    for i in range(100):

        # Normale Ausgabe oberhalb der Live-Anzeige
        if i % 1 == 0:
            live.console.print(f"[green]Event bei {i}%[/green]")

        # Nur die Live-Anzeige aktualisieren
        live.update(generate_display(i))

        time.sleep(0.1)