import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 30)  # Adjust 30 to match your LED count
pixels[0] = (255, 0, 0)  # Sets the first LED to red