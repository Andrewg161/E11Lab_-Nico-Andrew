import sys
import time
import datetime
import csv

import board
import busio
import adafruit_bme680
import serial
from adafruit_pm25.uart import PM25_UART

import RPi.GPIO as GPIO

# Setup Radiation Detector 
SIGNAL_PIN = 17
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN, GPIO.IN)

def pulse_detected(channel):
    global count
    count += 1

GPIO.add_event_detect(SIGNAL_PIN, GPIO.FALLING, callback=pulse_detected)

# Setup Sensors 
i2c = board.I2C()

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, None)

#  Setup CSV File
output_file = "final_full_data.csv"
csv_file = open(output_file, mode='w', newline='')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(["Timestamp", 
                     "Radiation_Counts", 
                     "Temperature (C)", "Humidity (%)", "Pressure (hPa)", "Gas (Ohm)",
                     "PM1.0", "PM2.5", "PM10"])

# Setup Runtime 
runtime_minutes = int(sys.argv[1])  # Pass runtime in minutes
end_time = time.time() + (runtime_minutes * 60)

last_save_time = time.time()

print("Starting full data collection...")

while time.time() < end_time:
    time.sleep(1)

    # Every 30 seconds save data
    if (time.time() - last_save_time) >= 30:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get Environmental Data 
        try:
            temperature = bme680.temperature
            humidity = bme680.relative_humidity
            pressure = bme680.pressure
            gas = bme680.gas
        except Exception as e:
            print("Error reading BME680:", e)
            temperature = humidity = pressure = gas = None

        # Get Air Quality Data 
        try:
            aqdata = pm25.read()
            pm10 = aqdata["pm10 standard"]
            pm25_val = aqdata["pm25 standard"]
            pm100 = aqdata["pm100 standard"]
        except Exception as e:
            print("Error reading PM2.5 sensor:", e)
            pm10 = pm25_val = pm100 = None

        # Save all data to CSV 
        csv_writer.writerow([timestamp, 
                              count, 
                              temperature, humidity, pressure, gas,
                              pm10, pm25_val, pm100])
        csv_file.flush()

        print(f"[{timestamp}] Counts: {count} | Temp: {temperature:.1f}C | Humidity: {humidity:.1f}% | PM2.5: {pm25_val}")

        count = 0  # Reset radiation counter
        last_save_time = time.time()

# Clean up after done 
csv_file.close()
GPIO.cleanup()
print("Finished full data collection :)")
