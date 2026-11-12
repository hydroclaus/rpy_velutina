import readchar

def getCurrentPosition ():

    try:
        f = open(".zero_max_position", "r")
        pos, max_pos = map(int, f.readline().split(","))
        f.close()
        return pos, max_pos
    except IOError:
        return 0, 0

def setCurrentPosition (steps, max_pos):

    f = open(".zero_max_position", "w+");
    f.write(str(steps) + "," + str(max_pos))
    f.close()

def moveBy(steps):
    pass

def calibrateRange ():
    print("KEEP A SAFETY DISTANCE OF ~5mm TO THE UPPER AND LOWER LIMITS OF THE RAIL!\n")
    print("Use arrow up/down to move to 0 position.")
    print("When 0 position reached, press 's' to save 0 position.\n")

    zeroPosition = None

    pos, max_pos = getCurrentPosition()

    while True:
        print(f"\rPosition: {pos}                     ", end="", flush=True)

        taste = readchar.readkey()

        if taste == readchar.key.UP:
            # print("Pfeil nach OBEN")
            moveBy(100)
            pos += 100
        elif taste == readchar.key.DOWN:
            # print("Pfeil nach UNTEN")
            moveBy(-100)
            pos -= 100
        elif taste.lower() == "s":
            if zeroPosition is None:
                pos = 0
                print("\rPosition set to 0.\n")
                print("Use arrow up/down to move to max position.")
                print("When max position reached, press 's' to save max position.\n")
                zeroPosition = True
            else:
                max_pos = pos
                print(f"\rMax position set to {max_pos}.\n")
                print("Calibration complete.\nReturning to 0 position...")
                moveBy(-pos)
                setCurrentPosition(0, max_pos)
                break
        elif taste == readchar.key.CTRL_C:
            print("Beendet.")
            break

calibrateRange()