import time
from machine import Pin, I2C
import BME280
import network
from umqtt.simple import MQTTClient
from secrets import SSID, PASSWORD, SERVER_PORT

# MQTT-Broker IP (IP-Adresse deines zentralen Raspberry Pi)
MQTT_SERVER = '192.168.48.116'

CLIENT_ID = "pico_9"
TOPIC = b"vegas/pico_9/temperatur"
KEEP_ALIVE = 120  # Keep-alive in Sekunden

DELTA_T_MINUTES = 1

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not SSID or SSID == 'your_ssid_here':
        raise RuntimeError('Missing Wi-Fi credentials. Set SSID and PASSWORD in the script.')

    print(f'Connecting to Wi-Fi SSID: {SSID}')

    while True:
        try:
            if not wlan.isconnected():
                wlan.connect(SSID, PASSWORD)

                # Wait up to 15 seconds for connection
                for _ in range(15):
                    if wlan.isconnected():
                        break
                    time.sleep(1)
                    print('.', end='')

            if wlan.isconnected():
                print()
                print('Connected to Wi-Fi')
                print('IP address:', wlan.ifconfig()[0])
                print()
                return
                
        except Exception as e:
            print(f'\nWi-Fi connection error: {e}')

        print('\nRetrying Wi-Fi connection in 5 seconds...')
        time.sleep(5)

def get_measurements(time_start):
    i2c = I2C(id=0, scl=Pin(5), sda=Pin(4))
    
    bme = BME280.BME280(i2c=i2c)
        
    seconds_since_start = time.time() - time_start

    # Get sensor readings, temp in °C, presssure in hPa, and humidity in %
    temp = float(bme.temperature) # + ' C'
    pres = float(bme.pressure) #+ ' hPa'
    try:
        hum = float(bme.humidity) #+ ' %'
    except:
        hum = 9999

    # Prepare data to send (omit time, will be added by server)
    line = f"{CLIENT_ID},{seconds_since_start:.2f},{temp:.2f},{pres:.2f},{hum:.2f}"
    
    return line

def main():
    connect_wifi()

    # MQTT Client initialisieren
    client = MQTTClient(CLIENT_ID, MQTT_SERVER, keepalive=KEEP_ALIVE)
    client.connect()
    print("Verbunden mit MQTT-Broker")

    try:
        time_start = time.time()
        while True:
            line = get_measurements(time_start)
            payload = str(line)
            client.publish(TOPIC, payload)
            print(f"Gesendet: {payload}")
            time.sleep(DELTA_T_MINUTES * 60)

    except Exception as e:
        print("Fehler:", e)
        client.disconnect()

if __name__ == '__main__':
    main()