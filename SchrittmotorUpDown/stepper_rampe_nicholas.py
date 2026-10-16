import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BOARD)

# TB6600 Treiber Setup
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

# Motor Setup
STEP_ANGLE = 1.8 # degree
RAMP_LENGTH = 600 # steps
MIN_RPM = 250
MAX_RPM = 800

# maximale Schrittzahl, die sich der Motor vom Nullpunkt weg bewegen darf
MAX_STEPS = 192000

# Frequenzberechnung
stepsPerRevolution = 360 / STEP_ANGLE

minFrequency = 1 / (MAX_RPM / 60 * stepsPerRevolution)
maxFrequency = 1 / (MIN_RPM / 60 * stepsPerRevolution)

rampSlope = (maxFrequency - minFrequency) / RAMP_LENGTH

def getCurrentPosition ():

    try:
        f = open("/home/claus/Repository/rpy_velutina/SchrittmotorUpDown/.position", "r")
        steps = int(f.read())
        f.close()
        return steps
    except:
        return 0

def setCurrentPosition (steps):

    f = open("/home/claus/Repository/rpy_velutina/SchrittmotorUpDown/.position", "w+");
    f.write(str(steps))
    f.close()

# dreht den Motor absolut an eine bestimmte Position
def moveTo (position):

    if (position < 0):
        position = 0
    if (position > MAX_STEPS):
        position = MAX_STEPS

    currentPosition = getCurrentPosition()
    steps = position - currentPosition

    return moveBy(steps)

# dreht den Motor relativ um eine bestimmte Anzahl Schritte
def moveBy (steps):

    GPIO.output(ENA, ENA_Locked)

    currentFreqency = maxFrequency
    currentPosition = getCurrentPosition()

    # relative Schrittzahl vorberechnen, die sich der Motor bewegen muss
    targetPosition = currentPosition + steps
    if (targetPosition > MAX_STEPS):
        steps = MAX_STEPS - currentPosition
    if (targetPosition < 0):
        steps = currentPosition * -1

    for i in range(abs(steps)):
        # if i in [x for x in range(0, abs(steps), 100)]:
        #     print(currentFreqency)
        
        # sofort stoppen, wenn sich der Motor über
        # die obere Grenze hinaus bewegen würde(0, abs(steps), 10)
        if (steps >= 0 and currentPosition >= MAX_STEPS):
            GPIO.output(ENA, ENA_Released)
            setCurrentPosition(currentPosition)
            return currentPosition

        # sofort stoppen, wenn sich der Motor über
        # die untere Grenze hinaus bewegen würde
        if (steps < 0 and currentPosition <= 0):
            GPIO.output(ENA, ENA_Released)
            setCurrentPosition(currentPosition)
            return currentPosition

        # Richtung festlegen
        if (steps < 0):
            GPIO.output(DIR, DIR_Right)
        else:
            GPIO.output(DIR, DIR_Left)

        # Schritt ausführen
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(currentFreqency / 2) # Hohe currentFrequency --> laengere Pause --> langsamere Drehung\Bewegung
        
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(currentFreqency / 2)
        
        # aktuelle Schrittposition mitzählen
        if (steps < 0):
            currentPosition -= 1
        else:
            currentPosition += 1

        # Rampensteigung auf aktuelle Frequenz anwenden
        if (abs(steps) > 2 * RAMP_LENGTH):
            if (i < RAMP_LENGTH):
                currentFreqency -= rampSlope
            else:
                if (i > abs(steps) - RAMP_LENGTH):
                    currentFreqency += rampSlope
        else:
            if (i < abs(steps) / 2):
                currentFreqency -= rampSlope
            else:
                currentFreqency += rampSlope

        #print(currentFreqency)

    setCurrentPosition(currentPosition)
    GPIO.output(ENA, ENA_Released)

    return currentPosition

# Parameter vom Scriptaufruf abfragen
if (len(sys.argv) != 2):
    print("Fehlender Parameter: Anzahl Schritte");
    sys.exit();

steps = int(sys.argv[1])
print("Schritte: " + str(steps))

# Funktion moveBy() mit dem Parameter füttern
# probiere auch: moveTo()
currentPosition = moveBy(steps)
print("Erreichte Position: " + str(currentPosition))