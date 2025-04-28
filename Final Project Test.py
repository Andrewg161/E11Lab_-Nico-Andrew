import sys
import time
import datetime
import csv

import board
import busio
import adafruit_lis3mdl

# Setup LIS3MDL Magnetometer 
i2c = board.I2C()
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)

# Setup CSV file
output_file = "magnetometer_data.csv"
csv_file = open(output_file, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Mag_X (uT)", "Mag_Y (uT)", "Mag_Z (uT)", "Mag_Total (uT)"])

# vSetup Runtime 
runtime_minutes = int(sys.argv[1])  # Pass runtime in minutes
end_time = time.time() + (runtime_minutes * 60)

print("Starting magnetometer data collection...")

# Main loop 
while time.time() < end_time:
    try:
        mag_x, mag_y, mag_z = lis3mdl.magnetic
        mag_total = (mag_x**2 + mag_y**2 + mag_z**2)**0.5
    except Exception as e:
        print("Error reading LIS3MDL:", e)
        mag_x = mag_y = mag_z = mag_total = None

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    csv_writer.writerow([timestamp, mag_x, mag_y, mag_z, mag_total])
    csv_file.flush()

    print(f"[{timestamp}] Mag_X: {mag_x:.2f} uT | Mag_Y: {mag_y:.2f} uT | Mag_Z: {mag_z:.2f} uT | Mag_Total: {mag_total:.2f} uT")

    time.sleep(1)  # Collect every second

# Clean up 
csv_file.close()

print("Finished magnetometer data collection:)")
