from machine import Pin, SPI, I2C, SoftI2C
import framebuf
import time
from scd30 import SCD30

# ---- OLED Driver (SH1107, SPI) ----
class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 64
        self.cs = Pin(9, Pin.OUT)
        self.rst = Pin(12, Pin.OUT)
        self.cs(1)
        self.spi = SPI(1, 20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
        self.dc = Pin(8, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()
        self.white = 0xffff
        self.black = 0x0000

    def write_cmd(self, cmd):
        self.cs(1); self.dc(0); self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1); self.dc(1); self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1); time.sleep(0.001)
        self.rst(0); time.sleep(0.01)
        self.rst(1)
        for cmd in [0xAE,0x00,0x10,0xB0,0xdc,0x00,0x81,0x6f,
                    0x21,0xa0,0xc0,0xa4,0xa6,0xa8,0x3f,0xd3,
                    0x60,0xd5,0x41,0xd9,0x22,0xdb,0x35,0xad,0x8a,0xAF]:
            self.write_cmd(cmd)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(64):
            col = 63 - page
            self.write_cmd(0x00 + (col & 0x0f))
            self.write_cmd(0x10 + (col >> 4))
            for num in range(16):
                self.write_data(self.buffer[page * 16 + num])

# ---- Init OLED ----
oled = OLED_1inch3()

# ---- Init SCD-30 via I2C ----
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=50000)
scd = SCD30(i2c, 0x61)

print("Waiting for SCD-30 to boot...")
time.sleep(8)

print("I2C scan:", [hex(addr) for addr in i2c.scan()])
started = False
for attempt in range(1, 6):
    try:
        scd.start_continous_measurement() # note: Waveshare typo, "continous" not "continuous"
        print("SCD-30 continuous measurement started")
        started = True
        break
    except OSError as err:
        print("SCD-30 start failed (attempt {}): {}".format(attempt, err))
        time.sleep(2)

if not started:
    print("Proceeding without explicit start command; sensor may already be running.")
    print("Trying SoftI2C fallback...")
    i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=50000)
    print("SoftI2C scan:", [hex(addr) for addr in i2c.scan()])
    scd = SCD30(i2c, 0x61)
    for attempt in range(1, 4):
        try:
            scd.start_continous_measurement()
            print("SCD-30 start succeeded on SoftI2C")
            break
        except OSError as err:
            print("SoftI2C start failed (attempt {}): {}".format(attempt, err))
            time.sleep(2)

# ---- Main Loop ----
print("Waiting for SCD-30...")
time.sleep(2)

while True:
    try:
        if scd.get_status_ready() == 1:
            co2, temp, hum = scd.read_measurement()
            print(f"CO2: {co2:.1f} ppm | Temp: {temp:.1f}C | Hum: {hum:.1f}%")
            oled.fill(0)
            oled.text("Air Quality", 20, 0, oled.white)
            oled.text("CO2:{:5.0f} ppm".format(co2), 0, 20, oled.white)
            oled.text("Tmp:{:5.1f} C".format(temp),  0, 36, oled.white)
            oled.text("Hum:{:5.1f} %".format(hum),   0, 52, oled.white)
            oled.show()
    except OSError as err:
        print("SCD-30 I2C runtime error:", err)
        time.sleep(2)
    time.sleep(2)