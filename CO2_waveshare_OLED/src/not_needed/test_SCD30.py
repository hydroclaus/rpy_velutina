from machine import I2C, Pin
from scd30 import SCD30

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=50000)
scd = SCD30(i2c, 0x61)
print(dir(scd))