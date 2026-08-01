
import os
import time
import network
import socket

from secrets import SSID, PASSWORD, SERVER_PORT

# for server (sending data)
# todo: 
#  - influxdb
#  - calibrate sensor
#  - run while raspberry ssh is disconnected (TMUX https://ttt.bartificer.net/book.html#ttt38)
#  - make connection to WLAN more robust


# # for WLAN
# SSID = os.getenv('CIRCUITPY_WIFI_SSID')
# PASSWORD = os.getenv('CIRCUITPY_WIFI_PASSWORD')
# SERVER_PORT = int(os.getenv('SENSOR_TCP_PORT', '8080'))



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
                time.sleep(60 * 5)
        except OSError as exc:
            print('Client disconnected:', exc)
        finally:
            client.close()


if __name__ == '__main__':
    connect_wifi()
    # prepare_csv()
    #start_tcp_server()