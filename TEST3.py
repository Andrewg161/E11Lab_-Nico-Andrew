import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)
