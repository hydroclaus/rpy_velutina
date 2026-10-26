import RPi.GPIO as GPIO
import sys
import time
import numpy as np

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
RAMP_LENGTH = None # 600 # steps
# MIN_RPM = 800 # Geschwindigkeit ueber MIN_RPM regeln, wenn RAMP_LENGTH = None
MAX_RPM = 800

# maximale Schrittzahl, die sich der Motor vom Nullpunkt weg bewegen darf
MAX_STEPS = 192000

# Frequenzberechnung
stepsPerRevolution = 360 / STEP_ANGLE

minFrequency = 1 / (MAX_RPM / 60 * stepsPerRevolution)
# maxFrequency = 1 / (MIN_RPM / 60 * stepsPerRevolution)

# if RAMP_LENGTH is not None:
#     rampSlope = (maxFrequency - minFrequency) / RAMP_LENGTH
# else:
#     rampSlope = None

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
    start = time.perf_counter()
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

        if rampSlope is not None:
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
        else:
            continue

        #print(currentFreqency)

    setCurrentPosition(currentPosition)
    GPIO.output(ENA, ENA_Released)
    
    ende = time.perf_counter()
    dauer = ende - start
    print(f"Zeit: {round(dauer, 2)}s")

    return currentPosition, dauer


durations = []
rpm_to_check = [rpm for rpm in np.arange(5.25, 0, -1)]
steps = 1600 # 0.5cm
start_position = getCurrentPosition()

print("Schritte für Messung: " + str(steps) + ", entspricht ca. " + str(steps/3200) + " cm")
print("Position: ", start_position)

for rpm in rpm_to_check:
    MIN_RPM = rpm
    maxFrequency = 1 / (MIN_RPM / 60 * stepsPerRevolution)

    if RAMP_LENGTH is not None:
        rampSlope = (maxFrequency - minFrequency) / RAMP_LENGTH
    else:
        rampSlope = None

    print("Aktuelle RPM: " + str(rpm))

    # Funktion moveBy() mit dem Parameter füttern
    
    currentPosition, dauer = moveBy(steps)
    durations.append(dauer)
    MIN_RPM = 800
    maxFrequency = 1 / (MIN_RPM / 60 * stepsPerRevolution)
    time.sleep(1)
    currentPosition, dauer = moveBy(-steps)
    time.sleep(1)
    print()

print("Messwerte speichern...")
print(rpm_to_check)
print(durations)
# name: rpm_time_relation_{starting position}_{steps per measurement}
with open(f"/home/claus/Repository/rpy_velutina/SchrittmotorUpDown/rpm_time_relation_{start_position}_{steps}.txt", "w") as f:
    f.write("RPM,Duration\n")
    for rpm, duration in zip(rpm_to_check, durations):
        f.writelines(f"{rpm},{duration}\n")
    f.close()