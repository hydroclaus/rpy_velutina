"""
I'll help you create Python code for displaying moving rainbow colors on your 12mm LED pixels with a Raspberry Pi Pico 2. These are likely WS2812B (NeoPixel) LEDs.Rainbow LED Pixels - Raspberry Pi Pico 2Code 

import machine
import neopixel
import time

# Configuration
PIN = 0  # GPIO pin connected to LED data line
NUM_LEDS = 50  # Number of LEDs in your strip
BRIGHTNESS = 0.3  # 0.0 to 1.0

# Initialize NeoPixel strip
np = neopixel.NeoPixel(machine.Pin(PIHere's example code for your LED pixels! Here's what you need to know:
Setup Instructions:

Wiring:

LED Data → GPIO0 (or change PIN in code)
LED 5V → VBUS (5V pin on Pico)
LED GND → GND on Pico


Install MicroPython:

Download the latest Raspberry Pi Pico 2 MicroPython firmware from micropython.org
Hold BOOTSEL button while plugging in USB, drag the .uf2 file onto the drive


Upload the code:

Use Thonny IDE (recommended) or any MicroPython editor
Save the file as main.py to run automatically on boot



Customization:

NUM_LEDS: Change to match your LED count
PIN: Change if using a different GPIO pin
BRIGHTNESS: Adjust from 0.0 to 1.0 (lower values draw less current)
wait: Adjust the delay values for faster/slower animations

The code includes three patterns:

rainbow_cycle() - Smooth rainbow that cycles through all colors
rainbow_chase() - Rainbow colors chase down the strip
rainbow_static() - Static rainbow display

Need help with a specific pattern or have different LED specifications? Let me know!

"""


import machine
import neopixel
import time

# Configuration
PIN = 0  # GPIO pin connected to LED data line
NUM_LEDS = 50  # Number of LEDs in your strip
BRIGHTNESS = 0.3  # 0.0 to 1.0

# Initialize NeoPixel strip
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return (pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return (255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return (0, pos * 3, 255 - pos * 3)

def apply_brightness(color, brightness):
	"""Apply brightness to RGB color tuple."""
	return tuple(int(c * brightness) for c in color)

def rainbow_cycle(wait=0.02):
	"""Draw rainbow that uniformly distributes across all pixels."""
	for j in range(255):
		for i in range(NUM_LEDS):
			pixel_index = (i * 256 // NUM_LEDS) + j
			color = wheel(pixel_index & 255)
			np[i] = apply_brightness(color, BRIGHTNESS)
		np.write()
		time.sleep(wait)

def rainbow_chase(wait=0.05):
	"""Rainbow colors chase down the strip."""
	for j in range(255):
		for i in range(NUM_LEDS):
			color = wheel((i + j) & 255)
			np[i] = apply_brightness(color, BRIGHTNESS)
		np.write()
		time.sleep(wait)

def rainbow_static():
	"""Display static rainbow across strip."""
	for i in range(NUM_LEDS):
		pixel_index = (i * 256 // NUM_LEDS)
		color = wheel(pixel_index & 255)
		np[i] = apply_brightness(color, BRIGHTNESS)
	np.write()

# Main loop
try:
	print("Starting rainbow patterns...")
	print(f"LEDs: {NUM_LEDS}, Pin: GPIO{PIN}, Brightness: {BRIGHTNESS}")
	
	while True:
		# Smooth rainbow cycle
		rainbow_cycle(wait=0.01)
		
		# Faster chase effect
		rainbow_chase(wait=0.02)
		
except KeyboardInterrupt:
	# Turn off all LEDs on exit
	for i in range(NUM_LEDS):
		np[i] = (0, 0, 0)
	np.write()
	print("\nProgram stopped")