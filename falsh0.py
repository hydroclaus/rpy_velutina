import board
import neopixel

pixels = neopixel.NeoPixel(board.D10, 25)  # Adjust 30 to match your LED count
pixels[0] = (255, 255, 255)  # Sets the first LED to red
pixels[1] = (0, 255, 0)      # Sets the second LED to green
pixels[2] = (0, 0, 255)      # Sets the third
