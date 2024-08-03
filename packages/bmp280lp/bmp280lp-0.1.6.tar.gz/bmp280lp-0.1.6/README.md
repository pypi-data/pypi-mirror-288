# bmp280lp

This library allows you to use BMP280 or BME280 sensor. Tested on Orange Pi 5 plus.<br>
Cette bibliothèque permet d'utiliser le capteur BMP280 ou BME280. Testé avec succés sur Orange Pi 5 plus.

## Installation

	pip install bmp280lp

## Usage example

	import sys
	import time
	from bmp280lp import BMP280

	# Reset the sensor
	def reset_sensor(sensor):
	    sensor.device_reset()
	    time.sleep(1)

	# Create an instance of the sensor with the appropriate parameters
	bmp = BMP280(port=2, address=0x77, mode=BMP280.NORMAL_MODE, 
	             oversampling_p=BMP280.OVERSAMPLING_P_x16, oversampling_t=BMP280.OVERSAMPLING_T_x2,
	             oversampling_h=BMP280.OVERSAMPLING_H_x1, filter=BMP280.IIR_FILTER_OFF, standby=BMP280.T_STANDBY_1000)

	reset_sensor(bmp)

	# Wait a few moments to ensure the sensor is properly initialized
	time.sleep(1)

	# Read pressure and temperature
	pressure = bmp.read_pressure()
	temp = bmp.read_temperature()

	# Format the output to one decimal place
	print(f"Pressure (hPa): {pressure:.1f}")
	print(f"Temperature (°C): {temp:.1f}")

	# Read humidity if the sensor is a BME280
	if bmp.is_bme280:
	    humidity = bmp.read_humidity()
	    print(f"Humidity (%): {humidity:.1f}")
	else:
	    print("The sensor is not a BME280, humidity measurement not available.")


## Documentation

Parameter Documentation

The BMP280 class offers several configuration parameters that allow you to customize the behavior of the sensor. Here is a detailed description of each of these parameters:

    Port: The I2C port used
    Address: The address of the sensor, typically 0x76 or 0x77

1. mode

The operating mode of the sensor. Possible values are:

    BMP280.SLEEP_MODE (0b00): The sensor is in sleep mode.
    BMP280.FORCED_MODE (0b01): The sensor performs a single measurement when forced.
    BMP280.NORMAL_MODE (0b11): The sensor performs continuous measurements.

2. oversampling_p

The oversampling factor for pressure measurements. The higher the factor, the greater the accuracy, but the measurement time also increases. Possible values are:

    BMP280.OVERSAMPLING_P_NONE (0b000): No pressure measurement.
    BMP280.OVERSAMPLING_P_x1 (0b001): Oversampling x1.
    BMP280.OVERSAMPLING_P_x2 (0b010): Oversampling x2.
    BMP280.OVERSAMPLING_P_x4 (0b011): Oversampling x4.
    BMP280.OVERSAMPLING_P_x8 (0b100): Oversampling x8.
    BMP280.OVERSAMPLING_P_x16 (0b101): Oversampling x16.

3. oversampling_t

The oversampling factor for temperature measurements. The higher the factor, the greater the accuracy, but the measurement time also increases. Possible values are:

    BMP280.OVERSAMPLING_T_NONE (0b000): No temperature measurement.
    BMP280.OVERSAMPLING_T_x1 (0b001): Oversampling x1.
    BMP280.OVERSAMPLING_T_x2 (0b010): Oversampling x2.
    BMP280.OVERSAMPLING_T_x4 (0b011): Oversampling x4.
    BMP280.OVERSAMPLING_T_x8 (0b100): Oversampling x8.
    BMP280.OVERSAMPLING_T_x16 (0b101): Oversampling x16.

4. filter

The IIR (Infinite Impulse Response) filter coefficient. This helps smooth the measurement data by reducing rapid variations due to noise. Possible values are:

    BMP280.IIR_FILTER_OFF (0b000): Filtering disabled.
    BMP280.IIR_FILTER_x2 (0b001): Filter coefficient x2.
    BMP280.IIR_FILTER_x4 (0b010): Filter coefficient x4.
    BMP280.IIR_FILTER_x8 (0b011): Filter coefficient x8.
    BMP280.IIR_FILTER_x16 (0b100): Filter coefficient x16.

5. standby

The standby time between measurements in normal mode. The longer the standby time, the lower the power consumption, but the measurement rate is also reduced. Possible values are:

    BMP280.T_STANDBY_0p5 (0b000): Standby time of 0.5 ms.
    BMP280.T_STANDBY_62p5 (0b001): Standby time of 62.5 ms.
    BMP280.T_STANDBY_125 (0b010): Standby time of 125 ms.
    BMP280.T_STANDBY_250 (0b011): Standby time of 250 ms.
    BMP280.T_STANDBY_500 (0b100): Standby time of 500 ms.
    BMP280.T_STANDBY_1000 (0b101): Standby time of 1000 ms.
    BMP280.T_STANDBY_2000 (0b110): Standby time of 2000 ms.
    BMP280.T_STANDBY_4000 (0b111): Standby time of 4000 ms.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

This library was developed by Laurent Pastor. It's a fork off bmp-280 library with adding the setting address.
