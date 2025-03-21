import RPi.GPIO as GPIO
import datetime

SIGNAL_PIN = 2
count = 0

def pulse_detected(channel):
    global count
    count += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Pulse detected at", timestamp)

#The Set up for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SIGNAL_PIN, GPIO.FALLING, callback=pulse_detected)
print("Running")

start_time = datetime.datetime.now()
count = 0

# While loop 
while True:
    current_time = datetime.datetime.now()
    elapsed_time = (current_time - start_time).seconds

    if elapsed_time < 60:
        if GPIO.input(SIGNAL_PIN) == GPIO.LOW:
            count += 1
    else:
        print("Counts in the last minute:", count)
        count = 0 
        start_time = datetime.datetime.now() 
        
GPIO.cleanup()


