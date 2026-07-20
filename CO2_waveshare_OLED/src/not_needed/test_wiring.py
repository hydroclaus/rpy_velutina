from machine import I2C, Pin
import time

combos = [
    (0, 0, 1),   # I2C0, GP0, GP1
    (0, 4, 5),   # I2C0, GP4, GP5
    (0, 8, 9),   # I2C0, GP8, GP9
    (1, 2, 3),   # I2C1, GP2, GP3
    (1, 6, 7),   # I2C1, GP6, GP7
    (1, 10, 11), # I2C1, GP10, GP11
]

for bus, sda, scl in combos:
    try:
        i2c = I2C(bus, sda=Pin(sda), scl=Pin(scl), freq=10000)
        devices = i2c.scan()
        if devices:
            print(f"FOUND on I2C{bus} SDA=GP{sda} SCL=GP{scl}: {[hex(d) for d in devices]}")
        else:
            print(f"Nothing on I2C{bus} SDA=GP{sda} SCL=GP{scl}")
    except Exception as e:
        print(f"Error on I2C{bus} SDA=GP{sda} SCL=GP{scl}: {e}")
    time.sleep(0.2)