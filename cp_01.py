import board
import adafruit_ws2801

odata = board.MOSI
oclock = board.SCLK

numleds = 25
bright = 0.5
leds = adafruit_ws2801.WS2801(oclock, odata, numleds, brightness=bright, auto_write=False)

# fills the first one blue
leds[3] = 0xff0000
leds[4] = (0, 0, 255)	# Set the first LED blue
leds[5] = 0x00ff00	# Set the second LED Green
# leds.show()

# fills all blue
# Use an RGB Tuple
# leds.fill((0, 0, 0))
# leds.show()

# leds[6:9] = ((255, 0, 0),
#              (0, 255, 0),
#              (0, 0, 255))



leds.show()