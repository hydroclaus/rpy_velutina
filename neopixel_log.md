## 2025-12-02

## made new environment

    python3 -m venv --system-site-packages ./venv

    source venv/bin/activate

##  installed packages

    pip install rpi_ws281x
    pip install neopixel
    pip install adafruit-circuitpython-neopixel

the third and latest version seems the most recent [link to docs](https://docs.circuitpython.org/projects/neopixel/en/latest/)


## Raspberry
generally, I am following [the approach described here](https://suntechlite.com/how-to-control-ws2812-led-strips-with-raspberry-pi/), particularly [this raspberry wiring diagram](https://cdn-learn.adafruit.com/assets/assets/000/094/851/original/led_pixels_python-hardware-wiring_bb.jpg?1600464207)

Some useful background information, even though not specifically on the ws281x but a similar teaching thing [can be found here: Pure Python library to drive APA102 LED stripes; Use with Raspberry Pi.](https://github.com/tinue/apa102-pi)

With "Hyperion", selecting colours is more interactive: [Jetzt wird’s bunt! Ambilight-Software Hyperion in Openelec installieren – Teil 2 – PowerPi](http://powerpi.de/jetzt-wirds-bunt-ambilight-software-hyperion-in-openelec-installieren-teil-2/)

This looks interesting: [vanshksingh/Pi5Neo: Library to Control Neopixel on Raspberry Pi 5 using python](https://github.com/vanshksingh/Pi5Neo)

## Hardware Setup

### Pixels

- I have Adafruit 12mm Diffuse Thin Digital RGB LED Pixel (strand of 25), bought at [berrybase](https://www.berrybase.de/en/adafruit-12mm-diffuse-thin-digital-rgb-led-pixel-strand-of-25?srsltid=AfmBOorEbchmwN7pkotycAA0bx2FmjInpKA0F4iBzgphC3qz--NRGHUE).
- this is their description at [Adafruit](https://learn.adafruit.com/12mm-led-pixels?view=all). Here it says that they do contain a **WS2801 LED** driver chip. It also says they would work with the [Adafruit Circuit Python WS2801 module](https://github.com/adafruit/Adafruit_CircuitPython_WS2801)

### Raspberry
- red and blue are connected to external power
- blue is also connected to ground `PIN3`
- yellow is in `GPIO 10 MOSI (SPI 0)`
- green is in `GPIO 11 SCLK (SPI0)`
