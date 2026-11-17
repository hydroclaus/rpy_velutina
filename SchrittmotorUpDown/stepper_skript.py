import RPi.GPIO as GPIO
import sys
import time
import readchar

######################################################################
############################### SET UP ###############################

GPIO.setmode(GPIO.BOARD)

# TB6600 Driver Setup
# Motor 1
DIR = 33
PUL = 35
ENA = 37
# Motor 2
DIR2 = ...
PUL2 = ...
ENA2 = ...

DIR_Left = GPIO.HIGH
DIR_Right = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
# Motor 1
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
# Motor 2
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(PUL2, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)

# Motor Setup
STEP_ANGLE = 1.8 # degree

stepsPerRevolution = 360 / STEP_ANGLE

######################################################################
############################## FUNCTIONS #############################

def readInstructions ():
    with open(".sequence", "r") as f:
        tasks = f.readlines()
    return tasks[1:]

def getCurrentPosition ():
    try:
        f = open(".position", "r")
        pos1, pos2 = map(int, f.readline().split(","))
        f.close()
        return pos1, pos2
    except:
        return 0, 0

def setCurrentPosition (pos1, pos2):
    f = open(".position", "w+");
    f.write(str(pos1) + "," + str(pos2))
    f.close()

def getMaxSteps ():
    try:
        f = open(".maxSteps", "r")
        max1, max2 = map(int, f.readline().split(","))
        f.close()
        return max1, max2
    except:
        return 0, 0

def setMaxSteps (max1, max2):
    f = open(".maxSteps", "w+");
    f.write(str(max1) + "," + str(max2))
    f.close()

# turn motor by number of steps
def moveBy (steps, motorNr):
    if motorNr == 1:
        GPIO.output(ENA, ENA_Locked)
    elif motorNr == 2:
        GPIO.output(ENA2, ENA_Locked)
    elif motorNr == 3:
        GPIO.output(ENA, ENA_Locked)
        GPIO.output(ENA2, ENA_Locked)

    currentPosition1, currentPosition2 = getCurrentPosition()

    # calculate relative steps
    # targetPosition = currentPosition + steps
    # if (targetPosition > MAX_STEPS):
    #     steps = MAX_STEPS - currentPosition
    # if (targetPosition < 0):
    #     steps = currentPosition * -1

    # start timer
    start = time.perf_counter()

    for i in range(abs(steps)):
        
        # stop if upper limit reached
        # if (steps >= 0 and currentPosition >= MAX_STEPS):
        #     GPIO.output(ENA, ENA_Released)
        #     setCurrentPosition(currentPosition)
        #     return currentPosition

        # stop if lower limit reached
        # if (steps < 0 and currentPosition <= 0):
        #     GPIO.output(ENA, ENA_Released)
        #     setCurrentPosition(currentPosition)
        #     return currentPosition

        # set direction to move (up or down)
        if (steps < 0):
            if motorNr == 1:
                GPIO.output(DIR, DIR_Right)
            elif motorNr == 2:
                GPIO.output(DIR2, DIR_Right)
            elif motorNr == 3:
                GPIO.output(DIR, DIR_Right)
                GPIO.output(DIR2, DIR_Right)
        else:
            if motorNr == 1:
                GPIO.output(DIR, DIR_Left)
            elif motorNr == 2:
                GPIO.output(DIR2, DIR_Left)
            elif motorNr == 3:
                GPIO.output(DIR, DIR_Left)
                GPIO.output(DIR2, DIR_Left)

        # execute steps
        if motorNr == 1:
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(frequency / 2) # high frequency --> longer pause --> slow move
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(frequency / 2)
        elif motorNr == 2:
            GPIO.output(PUL2, GPIO.HIGH)
            time.sleep(frequency / 2) # high frequency --> longer pause --> slow move
            GPIO.output(PUL2, GPIO.LOW)
            time.sleep(frequency / 2)
        elif motorNr == 3:
            GPIO.output(PUL, GPIO.HIGH)
            GPIO.output(PUL2, GPIO.HIGH)
            time.sleep(frequency / 2) # high frequency --> longer pause --> slow move
            GPIO.output(PUL, GPIO.LOW)
            GPIO.output(PUL2, GPIO.LOW)
            time.sleep(frequency / 2)
        
        # count current steps
        if (steps < 0):
            if motorNr == 1:
                currentPosition1 -= 1
            elif motorNr ==2:
                currentPosition2 -= 1
            elif motorNr == 3:
                currentPosition1 -= 1
                currentPosition2 -= 1
        else:
            if motorNr == 1:
                currentPosition1 += 1
            elif motorNr ==2:
                currentPosition2 += 1
            elif motorNr == 3:
                currentPosition1 += 1
                currentPosition2 += 1

    setCurrentPosition(currentPosition1, currentPosition2)
    
    if motorNr == 1:
        GPIO.output(ENA, ENA_Released)
    elif motorNr == 2:
        GPIO.output(ENA2, ENA_Released)
    elif motorNr == 3:
        GPIO.output(ENA, ENA_Released)
        GPIO.output(ENA2, ENA_Released)

    # end timer
    end = time.perf_counter()
    time_needed = end - start
    # print(f"Time needed: {round(time_needed, 2)}s")

def calibrateRange (motorNr):
    print("\n######### KEEP A SAFETY DISTANCE OF ~5mm TO THE UPPER AND LOWER LIMIT OF THE RAIL! #########\n")
    print("Use arrow up/down to move to 0 position.")
    print("When 0 position reached, press 's' to save 0 position.\n")

    zeroPosition = None

    currentPosition1, currentPosition2 = getCurrentPosition()
    max1, max2 = getMaxSteps()

    while True:
        if motorNr == 1:
            print(f"\rPosition: {currentPosition1}                     \033[0J", end="", flush=True)
        elif motorNr == 2:
            print(f"\rPosition: {currentPosition2}                     \033[0J", end="", flush=True)

        taste = readchar.readkey()

        if taste == readchar.key.UP:
            # print("Pfeil nach OBEN")
            moveBy(100, motorNr)
            if motorNr == 1:
                currentPosition1 += 100
            elif motorNr == 2:
                currentPosition2 += 100
            setCurrentPosition(currentPosition1, currentPosition2)
        elif taste == readchar.key.DOWN:
            # print("Pfeil nach UNTEN")
            moveBy(-100, motorNr)
            if motorNr == 1:
                currentPosition1 -= 100
            elif motorNr == 2:
                currentPosition2 -= 100
            setCurrentPosition(currentPosition1, currentPosition2)
        elif taste.lower() == "s":
            if zeroPosition is None:
                if motorNr == 1:
                    currentPosition1 = 0
                elif motorNr == 2:
                    currentPosition2 = 0
                setCurrentPosition(currentPosition1, currentPosition2)
                print("\rPosition set to 0.\n")
                time.sleep(1)
                print("Use arrow up/down to move to max position.")
                print("When max position reached, press 's' to save max position.\n")
                zeroPosition = True
            else:
                if motorNr == 1:
                    max1 = currentPosition1
                    print(f"\rMax position set to {max1}.\n")
                elif motorNr == 2:
                    max2 = currentPosition2
                    print(f"\rMax position set to {max2}.\n")
                setMaxSteps(max1, max2)
                time.sleep(1)
                print("Calibration complete.\nReturning to 0 position...")
                time.sleep(1)
                if motorNr == 1:
                    moveBy(-currentPosition1, motorNr)
                elif motorNr == 2:
                    moveBy(-currentPosition2, motorNr)
                break
        elif taste == readchar.key.CTRL_C:
            print("Beendet.")
            break

def checkSequence(tasks, max1, max2):    
    currentPosition1, currentPosition2 = getCurrentPosition()
    currentTask = 0

    # Check, if Sequence is within limits
    for task in tasks:
        currentTask += 1
        distance, _, _ = task.strip().split(",") # cm
        currentPosition1 += int(distance)*3200
        currentPosition2 += int(distance)*3200
        if currentPosition1 > max1:
            raise Warning(f"Sequence will exceed max position of motor nr. 1 while performing task {currentTask}!")
        if currentPosition2 > max2:
            raise Warning(f"Sequence will exceed max position of motor nr. 2 while performing task {currentTask}!")
        if currentPosition1 < 0:
            raise Warning(f"Sequence will fall below 0 position of motor nr. 1 while performing task {currentTask}!")
        if currentPosition2 < 0:
            raise Warning(f"Sequence will fall below 0 position of motor nr. 2 while performing task {currentTask}!")

######################################################################
################################ MAIN ################################

# MAX_STEPS = 192000 # max amount of steps, if slider at lowest position

cal = input("\nCalibrate stepper motor nr. 1 range?\n(y/n)\n")
if cal == "y":
    speed = 800
    rpm = 0.2667 * speed # not literal "rounds per minute"
    frequency = 1 / (rpm / 60 * stepsPerRevolution)
    try:
        calibrateRange(motorNr=1)
    except KeyboardInterrupt:
        pass
elif cal == "n":
    pass

cal = input("\nCalibrate stepper motor nr. 2 range?\n(y/n)\n")
if cal == "y":
    speed = 800
    rpm = 0.2667 * speed # not literal "rounds per minute"
    frequency = 1 / (rpm / 60 * stepsPerRevolution)
    try:
        calibrateRange(motorNr=2)
    except KeyboardInterrupt:
        pass
elif cal == "n":
    pass

# maximum steps the motor can move from 0 position
max1, max2 = getMaxSteps()

tasks = readInstructions()

print("\nCheck sequence...\n")
time.sleep(1)
checkSequence(tasks, max1, max2)

print("Starting sequence...\n")    
for task in tasks:
    distance, speed, pause = task.strip().split(",") # cm, cm/h, s
    
    distance = float(distance)
    speed = float(speed)
    pause = float(pause)
    
    steps = int(distance * 3200) # 3200 steps = 1 cm
    rpm = 0.2667 * speed # not literal "rounds per minute"
    frequency = 1 / (rpm / 60 * stepsPerRevolution)

    print("Move " + str(distance) + "cm with " + str(speed) + "cm/h")

    moveBy(steps, 3)

    print("Pause for " + str(pause) + "s")
    time.sleep(pause)