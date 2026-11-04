import RPi.GPIO as GPIO
import sys
import time

######################################################################
############################### SET UP ###############################

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

# maximale Schrittzahl, die sich der Motor vom Nullpunkt weg bewegen darf
MAX_STEPS = 192000

# Frequenzberechnung
stepsPerRevolution = 360 / STEP_ANGLE

######################################################################
############################## FUNCTIONS #############################

def getCurrentPosition ():

    try:
        f = open(".position", "r")
        steps = int(f.read())
        f.close()
        return steps
    except:
        return 0

def setCurrentPosition (steps):

    f = open(".position", "w+");
    f.write(str(steps))
    f.close()

# dreht den Motor relativ um eine bestimmte Anzahl Schritte
def moveBy (steps):
    GPIO.output(ENA, ENA_Locked)

    currentPosition = getCurrentPosition()

    # relative Schrittzahl vorberechnen, die sich der Motor bewegen muss
    targetPosition = currentPosition + steps
    if (targetPosition > MAX_STEPS):
        steps = MAX_STEPS - currentPosition
    if (targetPosition < 0):
        steps = currentPosition * -1

    # start timer
    start = time.perf_counter()

    for i in range(abs(steps)):
        
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
        time.sleep(frequency / 2) # Hohe frequency --> laengere Pause --> langsamere Drehung\Bewegung
        
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(frequency / 2)
        
        # aktuelle Schrittposition mitzählen
        if (steps < 0):
            currentPosition -= 1
        else:
            currentPosition += 1

    setCurrentPosition(currentPosition)
    GPIO.output(ENA, ENA_Released)

    # end timer
    ende = time.perf_counter()
    dauer = ende - start
    print(f"Benoetigte Zeit: {round(dauer, 2)}s")

    return currentPosition

######################################################################
################################ MAIN ################################

# get inputs from user
distance = int(input("Distanz in cm: "))
speed = int(input("Geschwindigkeit in cm/h: "))

steps = distance * 3200 # 3200 steps = 1 cm

RPM = 0.2667 * speed
frequency = 1 / (RPM / 60 * stepsPerRevolution)

print("Schritte zu bewegen: " + str(steps))

currentPosition = moveBy(steps)
print("Erreichte Position: " + str(currentPosition))