import network
import socket
import time
from machine import Pin, I2C
from bme680 import *
from secrets import SSID, PASSWORD, SERVER_PORT


# Constants
DEVICE_ID = 'Pico_Werkstatt_1'

#SERVER_IP = '192.168.178.47'
#PORT = SERVER_PORT


DELTA_T_MINUTES = 2


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


def main():
    # ---- Connect Wi-Fi ----
    wlan = connect_wifi()
    ip = wlan.ifconfig()[0]

    # ---- Start TCP server ----
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', SERVER_PORT))
    server.listen(1)
    print(f'TCP server listening on {ip}:{SERVER_PORT}')
    
    
    i2c = I2C(id=0, scl=Pin(5), sda=Pin(4))
    time_start = time.time()
    
    while True:
        try:
            client, addr = server.accept()
            print('Client connected:', addr)
            try:
                while True:
                    # Wait for data to be ready
                    #for _ in range(10):
                        #if scd.get_status_ready() == 1:
                            #break
                        #time.sleep(0.5)


                    bme = BME680_I2C(i2c=i2c)

                       
                    elapsed = time.time() - time_start

                    # Get sensor readings, temp in °C, presssure in hPa, and humidity in %
                    temp = str(round(bme.temperature, 2)) # + ' C'
                    hum = str(round(bme.humidity, 2)) #+ ' %'
                    pres = str(round(bme.pressure, 2)) #+ ' hPa'
                    gas = str(round(bme.gas/1000, 2)) #+ ' KOhms'
                    print(temp)

                    # Prepare data to send (omit time, will be added by server)
                    line = f"{DEVICE_ID},{elapsed:.2f},{float(temp[:-1]):.2f},{float(pres[:-3]):.2f},{float(hum[:-1]):.2f},{float(gas[:-1]):.2f}\n"

                    # Send to client as CSV
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