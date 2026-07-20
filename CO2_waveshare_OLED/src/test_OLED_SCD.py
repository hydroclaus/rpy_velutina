from machine import I2C, Pin
import time
from sh1106 import SH1106_I2C
from scd30 import SCD30

# Shared I2C bus
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=50000)  # 50kHz — SCD-30 prefers slower speeds

# Init display (128x64)
oled = SH1106_I2C(128, 64, i2c, addr=0x3C)

# Init SCD-30
scd = SCD30(i2c, 0x61)

def display_readings(co2, temp, hum):
    oled.fill(0)
    oled.text("Air Quality", 20, 0)
    oled.text("CO2:  {:4.0f}ppm".format(co2),  0, 20)
    oled.text("Temp: {:4.1f}C".format(temp),   0, 36)
    oled.text("Hum:  {:4.1f}%".format(hum),    0, 52)
    oled.show()

print("Waiting for SCD-30...")
time.sleep(2)

while True:
    if scd.get_data_ready():
        co2, temp, hum = scd.read_measurement()
        print(f"CO2: {co2:.1f} ppm | Temp: {temp:.1f}°C | Humidity: {hum:.1f}%")
        display_readings(co2, temp, hum)
    time.sleep(2)  # SCD-30 updates every 2 seconds by default