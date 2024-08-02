# bmp280lp

This library allows you to use BMP280 sensor. Tested on Orange Pi 5 plus.<br>
Cette bibliothèque permet d'utiliser le capteur BMP280. Testé avec succés sur Orange Pi 5 plus.

## Installation

pip install bmp280lp

## Usage example

from bmp280lp import bmp280

bmp = bmp280(port=2, address=0x77)

pressure = bmp.read_pressure()
temp = bmp.read_temperature()

print("Pressure (hPa): " + str(pressure))
print("Temperature (°C): " + str(temp))

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

This library was developed by Laurent Pastor. It's a fork off bmp-280 library with adding the setting address.
