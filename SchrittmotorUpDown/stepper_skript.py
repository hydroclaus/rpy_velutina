import RPi.GPIO as GPIO
import sys
import time

######################################################################
############################### SET UP ###############################

GPIO.setmode(GPIO.BOARD)

# TB6600 Driver Setup
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

# maximum steps the motor can move from 0 position
MAX_STEPS = 192000

stepsPerRevolution = 360 / STEP_ANGLE

######################################################################
############################## FUNCTIONS #############################

def readInstructions ():
    with open(".sequence", "r") as f:
        tasks = f.readlines()
    return tasks

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

# turn motor by number of steps
def moveBy (steps):
    GPIO.output(ENA, ENA_Locked)

    currentPosition = getCurrentPosition()

    # calculate relative steps
    targetPosition = currentPosition + steps
    if (targetPosition > MAX_STEPS):
        steps = MAX_STEPS - currentPosition
    if (targetPosition < 0):
        steps = currentPosition * -1

    # start timer
    start = time.perf_counter()

    for i in range(abs(steps)):
        
        # stop if upper limit reached
        if (steps >= 0 and currentPosition >= MAX_STEPS):
            GPIO.output(ENA, ENA_Released)
            setCurrentPosition(currentPosition)
            return currentPosition

        # stop if lower limit reached
        if (steps < 0 and currentPosition <= 0):
            GPIO.output(ENA, ENA_Released)
            setCurrentPosition(currentPosition)
            return currentPosition

        # set direction to move (up or down)
        if (steps < 0):
            GPIO.output(DIR, DIR_Right)
        else:
            GPIO.output(DIR, DIR_Left)

        # execute steps
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(frequency / 2) # high frequency --> longer pause --> slow move
        
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(frequency / 2)
        
        # count current steps
        if (steps < 0):
            currentPosition -= 1
        else:
            currentPosition += 1

    setCurrentPosition(currentPosition)
    GPIO.output(ENA, ENA_Released)

    # end timer
    end = time.perf_counter()
    time_needed = end - start
    print(f"Time needed: {round(time_needed, 2)}s")

    return

######################################################################
################################ MAIN ################################

tasks = readInstructions()
for task in tasks:
    distance, speed, pause = task.strip().split(",") # cm, cm/h, s
    
    distance = float(distance)
    speed = float(speed)
    pause = float(pause)
    
    steps = distance * 3200 # 3200 steps = 1 cm
    rpm = 0.2667 * speed # not literal "rounds per minute"
    frequency = 1 / (rpm / 60 * stepsPerRevolution)

    print("Move " + str(distance) + "cm with " + str(speed) + "cm/h")

    moveBy(steps)

    print("Pause for " + str(pause) + "s")
    time.sleep(pause)