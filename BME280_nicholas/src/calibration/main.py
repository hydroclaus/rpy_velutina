import time
from machine import Pin, I2C
import BME280

CLIENT_ID = "pico_..."

DELTA_T_SECONDS = 5

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
    line = f"{CLIENT_ID},{seconds_since_start:.2f},{temp:.2f},{pres:.2f},{hum:.2f}\n"
    
    return line

def main():
    time_start = time.time()

    with open(f"daten_{CLIENT_ID}.txt", "w") as f:
        f.write("DEVICE_ID,seconds_since_start,Temp [C],pres [hPa], relHum [%]\n")

    while True:
        try:
            line = get_measurements(time_start)
            
            with open(f"daten_{CLIENT_ID}.txt", "a") as f:
                f.write(line)

            time.sleep(DELTA_T_SECONDS)

        except Exception as e:
            print("Fehler:", e)
            print("Wait 10 seconds before next try...")
            time.sleep(10)

if __name__ == '__main__':
    main()