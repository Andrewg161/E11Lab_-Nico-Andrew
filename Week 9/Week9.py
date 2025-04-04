import RPi.GPIO as GPIO
import datetime
import time
import csv 

SIGNAL_PIN = 6
count = 0

# Making the CSV_Writerow
output_file = "counts_output.csv"
csv_file = open(output_file, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Counts"])

def pulse_detected(channel):
    global count
    count += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Pulse detected at", timestamp)

#The Set up for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN, GPIO.IN)
GPIO.add_event_detect(SIGNAL_PIN, GPIO.FALLING, callback=pulse_detected)
print("Running")

while True:
    time.sleep(10)
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 120:
        None  
    print("Counts in the last minute:", count)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_writer.writerow([timestamp, count]) #Adding the CSV Writer
    csv_file.flush()
    
    count = 0  
csv_file.close() #Close the file
