import storage
import digitalio
import board

# Pin prüfen (z.B. GP2). Wenn mit GND verbunden, bleibt PC-Schreibzugriff aktiv.
# Wenn offen, kann das CircuitPython-Skript Dateien schreiben.
pin = digitalio.DigitalInOut(board.GP2)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP

if pin.value:
    storage.remount("/", False) # PC verliert Schreibrechte, Pico übernimmt