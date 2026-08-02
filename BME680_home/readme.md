on the server (macMini, Raspberry)

    python Server_listening_BME.py

The BME680 measures four environmental variables:

Temperature — in °C
Humidity — relative humidity, in %
Barometric pressure — in hPa (or Pa)
Gas resistance (VOC/air quality) — measured via a MOX (metal oxide) sensor, used as a proxy for volatile organic compounds and indoor air quality

The first three are fairly standard and accurate. The gas resistance reading is the more unusual one — it's not a calibrated ppm value out of the box, but a resistance measurement (in Ω) that changes with VOC concentration. Bosch provides a proprietary algorithm (BSEC) that converts this raw resistance into an IAQ (Indoor Air Quality) index, but if you're just reading the sensor directly via I2C/SPI without BSEC, you get raw gas resistance and have to interpret/calibrate it yourself.