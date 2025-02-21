import sys
import time
import board
import adafruit_bme680
import busio
import serial
import csv
from adafruit_pm25.uart 
import PM25_UART

# Runtime of 10
run_time = 10  

# Testing argumement
if len(sys.argv) > 1:
    run_time = int(sys.argv[1])

# Initialize BME680 
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

# Initialize PM2.5
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin=None)

# Open CSV
file = open("sensor_data.csv", "w", newline="")
file_writer = csv.writer(file)
file_writer.writerow(["Time", "Temperature (C)", "Humidity (%)", "Pressure (hPa)", "Gas (Ohm)",
                      "PM10", "PM2.5", "PM100"])

print("Collecting data")

start_time = time.time()
while time.time() - start_time < run_time:
    elapsed_time = time.time() - start_time
    print("Time Elapsed:", elapsed_time, "sec")

    #  Weather data in values 
    temperature = bme680.temperature
    humidity = bme680.relative_humidity
    pressure = bme680.pressure
    gas = bme680.gas

    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Pressure:", pressure, "hPa")
    print("Gas Resistance:", gas, "Ohm")

    # Read Air Quality Data
    aqdata = pm25.read()
    pm10 = aqdata["pm10 standard"]
    pm25_value = aqdata["pm25 standard"]
    pm100 = aqdata["pm100 standard"]
    print("PM10:", pm10, "PM2.5:", pm25_value, "PM100:", pm100)

  
    # writer row
    file_writer.writerow([elapsed_time, temperature, humidity, pressure, gas, pm10, pm25_value, pm100])

    time.sleep(1)  

file.close()
print("Data collection complete. Check sensor_data.csv")
