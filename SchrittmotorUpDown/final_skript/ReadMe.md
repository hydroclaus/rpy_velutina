# This is a guidance for the stepper_skript to use for the stepper motor

This skript can be used to move the two motors up and down, by defining tasks (e.g. move the motor by 1 cm, with a speed of 50 cm/h, and pause for 10s after) in the .sequence file.

## Calibration
At each launch of the skript, it will ask to perform a calibration of the stepper motors to individually set the lowest and highest position the motors can reach. By pressing 'y' and ENTER, you will start the calibration (If not wanted, 'n' and ENTER).

The calibration is important, because the skript will check, if the upper or lower limit of the stepper motor range will be exceeded by your sequence.

## .sequence file explanation:
Each task is written in a new row under the header of the file. Together they build the sequence.
Distance, speed and the pause are separated by a comma (e.g. 1,50,10 for the example above).
The skript will work through the given sequence.

## .position and .maxSteps file explanation:
The "unit" the motor moves with is steps. 3200 steps equal 1 cm.
The maximum range of the larger stepper motor is 192000 steps, from the lowest position to the highest position, where the slider touches the bottom/top metal plate.

The current position (and zero position when calibrating) is saved in the .position file and the max position is saved in the .maxSteps file.