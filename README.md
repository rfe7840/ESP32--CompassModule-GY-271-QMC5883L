# CompassModule GY-271 with QMC5883L on ESP32 with Micropython

Micropythonscript for using GY-271 compass magnetometer with ESP32. Tested on AZ-Delivery GY-271 compass magnetometer module with QMC5883L chip.

# Hardware-Connection
The module has I2C communication lines(SDA, SCL), connect it to the I2C interfce of the ESP32 microcontroller. In this project Pins 22, 21 were used) Default I2C address of the module in this case was 13. Powersupply: 3.3 V in this Case GND to Ground

# Usage
Copy the QMC5883L.py to the ESP32. Then import it like in the example Script.
`from QMC5883L import QMC5883L 
qmc = QMC5883L()
qmc.read_Temperature()
qmc.heading()`
# Thanks to:
https://github.com/Slaveche90/gy271compass

https://github.com/robert-hh/QMC5883/blob/master/qmc5883.py

https://github.com/gvalkov/micropython-esp8266-hmc5883l/blob/master/hmc5883l.py

 
