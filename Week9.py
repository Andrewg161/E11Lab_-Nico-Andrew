import RPi.GPIO as GPIO
import datetime
import time

SIGNAL_PIN = 6
count = 0

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
#    start_time = datetime.datetime.now()
#    while (datetime.datetime.now() - start_time).seconds < 60:
#        None  # Don't sleep, keep checking
#    print("Counts in the last minute:", count)
#    count = 0  # Reset count for next minute

