import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D10, 25, 3, 1.0)  # Adjust 30 to match your LED count


# Cycle through colors
while True:
    pixels[::2] = [RED] * (len(pixels) // 2)
        time.sleep(2)
