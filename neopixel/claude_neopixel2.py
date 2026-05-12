import machine
import time

# Configuration
DATA_PIN = 0   # GPIO pin for LED data line (typically green wire)
CLOCK_PIN = 1  # GPIO pin for LED clock line (typically yellow wire)
NUM_LEDS = 25  # Number of LEDs in your strip
BRIGHTNESS = 1.0  # 0.0 to 1.0

class WS2801:
    """Driver for WS2801 LED strips."""
    
    def __init__(self, num_leds, data_pin, clock_pin):
        self.num_leds = num_leds
        self.spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0,
                               sck=machine.Pin(clock_pin),
                               mosi=machine.Pin(data_pin))
        self.buf = bytearray(num_leds * 3)
        self.clear()
    
    def set_pixel(self, index, r, g, b):
        """Set a single pixel color (RGB order for WS2801)."""
        if 0 <= index < self.num_leds:
            offset = index * 3
            self.buf[offset] = r
            self.buf[offset + 1] = g
            self.buf[offset + 2] = b
    
    def show(self):
        """Write buffer to LEDs."""
        self.spi.write(self.buf)
        time.sleep_us(500)  # Latch delay for WS2801
    
    def clear(self):
        """Clear all LEDs."""
        for i in range(len(self.buf)):
            self.buf[i] = 0
        self.show()

# Initialize LED strip
strip = WS2801(NUM_LEDS, DATA_PIN, CLOCK_PIN)

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
            r, g, b = wheel(pixel_index & 255)
            r, g, b = apply_brightness((r, g, b), BRIGHTNESS)
            strip.set_pixel(i, r, g, b)
        strip.show()
        time.sleep(wait)

def rainbow_chase(wait=0.05):
    """Rainbow colors chase down the strip."""
    for j in range(255):
        for i in range(NUM_LEDS):
            r, g, b = wheel((i + j) & 255)
            r, g, b = apply_brightness((r, g, b), BRIGHTNESS)
            strip.set_pixel(i, r, g, b)
        strip.show()
        time.sleep(wait)

def rainbow_static():
    """Display static rainbow across strip."""
    for i in range(NUM_LEDS):
        pixel_index = (i * 256 // NUM_LEDS)
        r, g, b = wheel(pixel_index & 255)
        r, g, b = apply_brightness((r, g, b), BRIGHTNESS)
        strip.set_pixel(i, r, g, b)
    strip.show()

def color_wipe(r, g, b, wait=0.05):
    """Wipe a color across all pixels."""
    r, g, b = apply_brightness((r, g, b), BRIGHTNESS)
    for i in range(NUM_LEDS):
        strip.set_pixel(i, r, g, b)
        strip.show()
        time.sleep(wait)

def theater_chase_rainbow(wait=0.1):
    """Rainbow theater chase effect."""
    for j in range(255):
        for q in range(3):
            for i in range(0, NUM_LEDS, 3):
                idx = i + q
                if idx < NUM_LEDS:
                    r, g, b = wheel((idx + j) % 255)
                    r, g, b = apply_brightness((r, g, b), BRIGHTNESS)
                    strip.set_pixel(idx, r, g, b)
            strip.show()
            time.sleep(wait)
            for i in range(0, NUM_LEDS, 3):
                idx = i + q
                if idx < NUM_LEDS:
                    strip.set_pixel(idx, 0, 0, 0)

# Main loop
try:
    print("Starting WS2801 rainbow patterns...")
    print(f"LEDs: {NUM_LEDS}, Data: GPIO{DATA_PIN}, Clock: GPIO{CLOCK_PIN}")
    print(f"Brightness: {BRIGHTNESS}")
    
    # Test: wipe red, green, blue
    print("Testing colors...")
    color_wipe(255, 0, 0, 0.02)  # Red
    time.sleep(0.3)
    color_wipe(0, 255, 0, 0.02)  # Green
    time.sleep(0.3)
    color_wipe(0, 0, 255, 0.02)  # Blue
    time.sleep(0.3)
    
    while True:
        # Smooth rainbow cycle
        rainbow_cycle(wait=0.01)
        
        # Faster chase effect
        rainbow_chase(wait=0.02)
        
        # Theater chase rainbow
        theater_chase_rainbow(wait=0.05)
        
except KeyboardInterrupt:
    # Turn off all LEDs on exit
    strip.clear()
    print("\nProgram stopped")