#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hello
"""
from secrets import SSID, PASSWORD, SERVER_PORT

import os
import time
import network
import socket

from machine import Pin, SPI, I2C
import framebuf
from scd30 import SCD30

__author__ = "Claus Haslauer (mail@planetwater.org)"
__version__ = "$Revision: 0.2 $"
__date__ = "datetime.date(2026,5,16)"
__copyright__ = "Copyright (c) 2026 Claus Haslauer"
__license__ = "Python"

DELTA_T_MINUTES = 5

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not SSID or SSID == 'your_ssid_here':
        raise RuntimeError('Missing Wi-Fi credentials. Set SSID and PASSWORD in the script.')

    print(f'Connecting to Wi-Fi SSID: {SSID}')
    wlan.connect(SSID, PASSWORD)

    # Wait up to 15 seconds for connection
    for _ in range(30):
        if wlan.isconnected():
            break
        time.sleep(0.5)
        print('.', end='')

    if not wlan.isconnected():
        raise RuntimeError('Failed to connect to Wi-Fi')

    print()
    print('Connected to Wi-Fi')
    print('IP address:', wlan.ifconfig()[0])
    return wlan


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


def init_scd30():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=10000)
    scd = SCD30(i2c, 0x61)

    print("Waiting for SCD-30 to boot...")
    time.sleep(3)

    for attempt in range(1, 6):
        try:
            scd.start_continous_measurement()
            print("SCD-30 continuous measurement started")
            return scd
        except OSError as err:
            print(f"SCD-30 start failed (attempt {attempt}): {err}")
            time.sleep(2)

    raise RuntimeError("Could not start SCD-30 after 5 attempts")


def main():
    # ---- Connect Wi-Fi ----
    wlan = connect_wifi()
    ip = wlan.ifconfig()[0]

    # ---- Init OLED ----
    oled = OLED_1inch3()
    oled.fill(0)
    oled.text("Connecting...", 0, 28, oled.white)
    oled.show()

    # ---- Init SCD-30 ----
    scd = init_scd30()
    time_start = time.time()

    # ---- Show IP on OLED ----
    oled.fill(0)
    oled.text("IP:", 0, 0, oled.white)
    oled.text(ip, 0, 12, oled.white)
    oled.text(f"Port:{SERVER_PORT}", 0, 24, oled.white)
    oled.show()

    # ---- Start TCP server ----
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', SERVER_PORT))
    server.listen(1)
    print(f'TCP server listening on {ip}:{SERVER_PORT}')

    while True:
        try:
            client, addr = server.accept()
            print('Client connected:', addr)
            try:
                while True:
                    # Wait for data to be ready
                    for _ in range(10):
                        if scd.get_status_ready() == 1:
                            break
                        time.sleep(0.5)

                    co2, temp, hum = scd.read_measurement()

                    if co2 is not None:
                        elapsed = time.time() - time_start

                        # Update OLED
                        oled.fill(0)
                        oled.text("CO2:{:5.0f} ppm".format(co2), 0, 0,  oled.white)
                        oled.text("Tmp:{:5.1f} C".format(temp),  0, 20, oled.white)
                        oled.text("Hum:{:5.1f} %".format(hum),   0, 36, oled.white)
                        oled.text("t:{:.0f} s".format(elapsed),  0, 52, oled.white)
                        oled.show()

                        print(f"CO2: {co2:.1f} ppm | Temp: {temp:.1f} C | Hum: {hum:.1f} %")

                        # Send to client as CSV
                        line = f'{elapsed:.2f},{co2:.2f},{temp:.2f},{hum:.2f}\n'
                        client.send(line.encode('utf-8'))

                    # SCD-30 default update interval is ~2 seconds
                    print("sleep {} minutes...".format(DELTA_T_MINUTES))
                    time.sleep(DELTA_T_MINUTES * 60)

            except OSError as err:
                print("Read error:", err)
            finally:
                client.close()
                print('Client disconnected')

        except OSError as err:
            print("Server error:", err)
            time.sleep(1)


if __name__ == '__main__':
    main()