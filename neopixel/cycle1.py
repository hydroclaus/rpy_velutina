import time
import board
import neopixel

RED = (0x10, 0, 0)

pixels = neopixel.NeoPixel(board.D10, 25)  # Adjust 30 to match your LED count
print(len(pixels)//2)

# Cycle through colors
while True:
    pixels[::2] = [RED] * (len(pixels) // 2)
    time.sleep(2)
time.sleep(1)