import time
from machine import Pin, I2C
import BME280
import gc

DELTA_T_SECONDS = 2

def get_measurements():
    i2c = I2C(id=0, scl=Pin(5), sda=Pin(4))
    
    bme = BME280.BME280(i2c=i2c)
        
    # Get sensor readings, temp in °C, presssure in hPa, and humidity in %
    temp = float(bme.temperature) # + ' C'
    pres = float(bme.pressure) #+ ' hPa'
    try:
        hum = float(bme.humidity) #+ ' %'
    except:
        hum = 9999

    # Prepare data to send (omit time, will be added by server)
    line = f"{temp:.2f},{pres:.2f},{hum:.2f}\n"
    
    return line

def main():
    while True:
        try:
            line = get_measurements()
            
            with open(f"cal_data.txt", "a") as f:
                f.write(line)

            print(f"Data written. {line}")
            gc.collect()
            time.sleep(DELTA_T_SECONDS)

        except Exception as e:
            print("Fehler:", e)
            print("Wait 10 seconds before next try...")
            time.sleep(10)

if __name__ == '__main__':
    main()