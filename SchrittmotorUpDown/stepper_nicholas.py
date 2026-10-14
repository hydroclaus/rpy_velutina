"""
https://www.heimkino-praxis.de/leinwand-maskierung-schrittmotor-steuerung/
"""
import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)

# Raspberry Pi Pin-Belegung für TB6600 Treiber
DIR = 33 # Direction (forward/backward)
PUL = 35 # Puls frequency (speed)
ENA = 37 # "Enable" --> Clutch (pressed (ENA on), no force --> neutral (motor off)... loose (ENA off), force --> activation (motor on))
ENDSTOP = 8 # Pin for light barrier (endstop)

DIR_Left = GPIO.HIGH
DIR_Right = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENDSTOP, GPIO.IN)

steps = int(sys.argv[1]) # Anzahl Schritte aus dem Parameter

# Motor aktivieren und halten
GPIO.output(ENA, ENA_Locked)

# Richtung festlegen
# GPIO.output(DIR, DIR_Left)

# Richtung abhängig von positivem oder negativem Wert
if (steps < 0):
    GPIO.output(DIR, DIR_Right)
else:
    GPIO.output(DIR, DIR_Left)

for i in range(abs(steps)):

    # stop if light barrier interrupted
    if (int(GPIO.input(ENDSTOP)) == 1):
        print("Light barrier interrupted")
        break
    
    # Puls modulieren
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(0.0001875)

    GPIO.output(PUL, GPIO.LOW)
    time.sleep(0.0001875)

# Motor freigeben
GPIO.output(ENA, ENA_Released)