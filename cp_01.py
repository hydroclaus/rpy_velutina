import board
import adafruit_ws2801

odata = board.MOSI
oclock = board.SCLK

numleds = 25
bright = 0.5
leds = adafruit_ws2801.WS2801(oclock, odata, numleds, brightness=bright, auto_write=False)

leds[0] = 0xff0000
leds.show()