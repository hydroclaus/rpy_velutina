# CO2 sensor with OLED display

[General overview: Getting Started with Raspberry Pi Pico and CircuitPython | Adafruit Learning System](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/overview)

## CO2 sensor
- [Arduino | Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor | Adafruit Learning System](https://learn.adafruit.com/adafruit-scd30/arduino)


## OLED display
- [Pico OLED 1.3 - Waveshare Wiki](https://www.waveshare.com/wiki/Pico-OLED-1.3)
- bought: [1.3" 64×128 OLED Display Modul für Raspberry Pi Pico - kaufen bei BerryBase](https://www.berrybase.de/1.3-64-128-oled-display-modul-fuer-raspberry-pi-pico?srsltid=AfmBOoqd9YH-tw9bBSp3oU1n8KDQBzAYYALFfsw69hVy52r-ZMbERuhM)

## Setup CO2 Sensor
There are two ways to operate

1. save data to Pico; then `boot.py` needs to be running (is executed on startup of Pico), which disables writing to Pico from attached computer (e.g., Mac, via USB) and `scd30_01.py` needs to be executed.
2. transfer data via WLAN to server (following this idea: [Real-Time Temperature Streaming on Raspberry Pi Pico W Using WebSockets](https://medium.com/@hnajjar3/real-time-temperature-streaming-on-raspberry-pi-pico-w-using-websockets-6c68a8bdbd06))
	- `scd30_02_WlanServer.py` needs to be running on Pico and `scd30_websockt.py` needs to be running on the server / main computer
    - prerequisites: 
		- on the pico: `board`, `busio`, `adafruit_scd30`, `wifi`, `socketpool`
		- on the server: `asyncio`
		- in order to manage prerequisites on the pico, circup is a nice tool, and can be installed on the server via `pip3 install circup`. Then, for example, the [asyncio library can be easily installed](https://docs.circuitpython.org/projects/asyncio/en/latest/)