import readchar

print("Drücke eine Pfeiltaste (STRG+C zum Beenden)...")

while True:
    # Wartet direkt auf den nächsten Tastendruck im Terminal
    taste = readchar.readkey()

    if taste == readchar.key.UP:
        print("Pfeil nach OBEN")
    elif taste == readchar.key.DOWN:
        print("Pfeil nach UNTEN")
    elif taste == readchar.key.LEFT:
        print("Pfeil nach LINKS")
    elif taste == readchar.key.RIGHT:
        print("Pfeil nach RECHTS")
    elif taste == readchar.key.CTRL_C:
        print("Beendet.")
        break