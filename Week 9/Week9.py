import RPi.GPIO as GPIO
import datetime
import time
import csv  # < added

SIGNAL_PIN = 6
count = 0

def pulse_detected(channel):
    global count
    count += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Pulse detected at", timestamp)

# The Set up for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN, GPIO.IN)
GPIO.add_event_detect(SIGNAL_PIN, GPIO.FALLING, callback=pulse_detected)
print("Running")

end_time = time.time() + 120  # 2 minutes total runtime

# added for saving data
output_file = open("week11_data.csv", "w", newline="")
writer = csv.writer(output_file)
writer.writerow(["Timestamp", "Counts"])

while time.time() < end_time:
    time.sleep(10)
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 60:
        None  
    print("Counts in the last minute:", count)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # added
    writer.writerow([timestamp, count])  # added
    count = 0

#added after loop ends
output_file.close()
print("Data saved to week11_data.csv")
