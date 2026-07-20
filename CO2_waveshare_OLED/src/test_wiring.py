from machine import I2C, Pin

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=50000)
devices = i2c.scan()
print("Found devices:", [hex(d) for d in devices])