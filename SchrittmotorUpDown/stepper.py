"""
https://www.heimkino-praxis.de/leinwand-maskierung-schrittmotor-steuerung/
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Raspberry Pi Pin-Belegung für TB6600 Treiber
DIR = 33
PUL = 35
ENA = 37

DIR_Left = GPIO.HIGH
DIR_Right = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Motor aktivieren und halten
GPIO.output(ENA, ENA_Locked)

# Richtung festlegen
GPIO.output(DIR, DIR_Left)

for i in range(200):

    # Puls modulieren
    GPIO.output(PUL, GPIO.HIGH)
    time.sleep(0.0001875)

    GPIO.output(PUL, GPIO.LOW)
    time.sleep(0.0001875)

# Motor freigeben
GPIO.output(ENA, ENA_Released)