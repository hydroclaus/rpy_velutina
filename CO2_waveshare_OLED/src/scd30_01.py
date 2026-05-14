# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import os
import time

# for SCD-30
try:
    import board
    import busio
    import adafruit_scd30
    import wifi
except ImportError as exc:
    raise RuntimeError(
        'This script must run on a CircuitPython device with the wifi and adafruit_scd30 libraries installed.'
    ) from exc

# for server (sending data)
# todo: influxdb


# for WLAN
SSID = os.getenv('CIRCUITPY_WIFI_SSID')
PASSWORD = os.getenv('CIRCUITPY_WIFI_PASSWORD')



def connect_wifi():
    if not SSID or not PASSWORD:
        raise RuntimeError(
            'Missing Wi-Fi credentials. Set CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD in settings.toml.'
        )

    print(f'Connecting to Wi-Fi SSID: {SSID}')
    wifi.radio.connect(SSID, PASSWORD)

    while not wifi.radio.ipv4_address:
        time.sleep(0.1)

    print('Connected to Wi-Fi')
    print('IP address:', wifi.radio.ipv4_address)



def gather_data():
    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    #i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    i2c = busio.I2C(board.GP5, board.GP4, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)

    # Create output file with headers
    with open("/sensor_data.csv", "w") as fp:
        fp.write("datetime,CO2 [PPM],Temp [C],relHum [%]\n")

    start_time = time.monotonic()

    while True:
        # since the measurement interval is long (2+ seconds) we check for new data before reading
        # the values, to ensure current readings.
        if scd.data_available:

            
            # Write to file
            elapsed = time.monotonic() - start_time        
            
            #print("Data Available!")
            print("time elapsed: seconds since start", elapsed)
            print(f"    CO2: {scd.CO2:f} PPM")
            print(f"    Temperature: {scd.temperature:0.2f} degrees C")
            print(f"    Humidity: {scd.relative_humidity:0.2f} % rH")
            print("")
            print("     ... Waiting for new data...")
            print("")
            
            
            
            with open("/sensor_data.csv", "a") as fp:
                fp.write(f"{elapsed:.2f},{scd.CO2:f},{scd.temperature:0.2f},{scd.relative_humidity:0.2f}\n")

        # 5 minutes in seconds
        dt = 5 * 60.0
        time.sleep(dt)


if __name__ == "__main__":
    connect_wifi()
    # gather_data()