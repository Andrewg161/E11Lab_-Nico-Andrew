import adafruit_bme680
import time
import board

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

start_time = time.time()
run_time = 30
while time.time() - start_time < run_time:
	elasped_time = time.time() - start_time
	print("\nTemperature: %0.1f C" % bme680.temperature)
	print("Gas: %d ohm" % bme680.gas)
	print("Humidity: %0.1f %%" % bme680.relative_humidity)
	print("Pressure: %0.3f hPa" % bme680.pressure)
	print("Altitude = %0.2f meters" % bme680.altitude)
	
	
	print("Start time:", time.ctime(start_time))
	time.sleep(2)
	end_time = time.time()
	print("End time:", time.ctime(end_time))
	print("Total time:", end_time - start_time, "seconds")
	
