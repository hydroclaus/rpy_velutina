import machine
import utime

led = machine.Pin("LED", machine.Pin.OUT)
while True:
    led.toggle()
    utime.sleep(0.5)