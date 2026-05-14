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
    import socketpool

except ImportError as exc:
    raise RuntimeError(
        'This script must run on a CircuitPython device with wifi, socketpool, and adafruit_scd30 libraries installed.'
    ) from exc

# for server (sending data)
# todo: influxdb


# for WLAN
SSID = os.getenv('CIRCUITPY_WIFI_SSID')
PASSWORD = os.getenv('CIRCUITPY_WIFI_PASSWORD')
SERVER_PORT = int(os.getenv('SENSOR_TCP_PORT', '8080'))



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


def init_sensor():
    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    # i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    i2c = busio.I2C(board.GP5, board.GP4, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)

    return scd, time.monotonic()


def read_measurement(scd, start_time):
    # Return None when no fresh sample is available yet.
    if not scd.data_available:
        return None

    elapsed = time.monotonic() - start_time
    co2 = scd.CO2
    temperature = scd.temperature
    humidity = scd.relative_humidity

    print('time elapsed: seconds since start', elapsed)
    print(f'    CO2: {co2:f} PPM')
    print(f'    Temperature: {temperature:0.2f} degrees C')
    print(f'    Humidity: {humidity:0.2f} % rH')
    print('')

    return elapsed, co2, temperature, humidity


def append_csv(elapsed, co2, temperature, humidity):
    with open('/sensor_data.csv', 'a') as fp:
        fp.write(f'{elapsed:.2f},{co2:f},{temperature:0.2f},{humidity:0.2f}\n')


def prepare_csv():
    with open('/sensor_data.csv', 'w') as fp:
        fp.write('datetime,CO2 [PPM],Temp [C],relHum [%]\n')


def start_tcp_server(port=SERVER_PORT):
    pool = socketpool.SocketPool(wifi.radio)
    server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f'TCP server listening on {wifi.radio.ipv4_address}:{port}')

    scd, start_time = init_sensor()

    while True:
        client, addr = server.accept()
        print('Client connected:', addr)
        try:
            while True:
                sample = read_measurement(scd, start_time)
                if sample is not None:
                    elapsed, co2, temperature, humidity = sample
                    #append_csv(elapsed, co2, temperature, humidity)
                    line = f'{elapsed:.2f},{co2:f},{temperature:0.2f},{humidity:0.2f}\n'
                    client.send(line.encode('utf-8'))
                time.sleep(1)
        except OSError as exc:
            print('Client disconnected:', exc)
        finally:
            client.close()


if __name__ == '__main__':
    connect_wifi()
    # prepare_csv()
    start_tcp_server()