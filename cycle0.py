import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D10, 25)  # Adjust 30 to match your LED count


# Cycle through colors
while True:
    pixels.fill((255, 0, 0))  # Red
    time.sleep(1)
    pixels.fill((0, 255, 0))  # Green
    time.sleep(1)
    pixels.fill((0, 0, 255))  # Blue
    time.sleep(1)
    pixels.fill((0, 255, 0))
time.sleep(1)