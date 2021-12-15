# Reading sensors using I2C

## Goals

* Learn the API provided by ESP-IDF to use the I2C serial buses
* Read the temperature from sensor HTS221 in the board

## Documentation

To complete this assignment, you may need to check the slides discuss in the lectures and the official API documentation:

* [ESP-IDF API for I2C](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html)
* [HTS221 sensor data sheet](https://www.st.com/resource/en/datasheet/hts221.pdf)
* [SoC reference](https://docs.espressif.com/projects/espressif-esp-iot-solution/en/latest/hw-reference/ESP32-MeshKit-Sense_guide.html)

## Reading the temperature sensor

### Obtaining information about the sensor

Using the data sheet, search the infomation required to use the sensor: slave address, addresses of the control registers, how to perform a write and a read through I2C.


!!! danger "Stop and sync "
     All previous exercises **must be finished DURING the lecture (not afterwards)** and shown to the teacher during the Zoom meeting. 

### Reading the device identification

In this step you will use the I2C bus to read the device identificación of the temperature sensor, that is stored in its WHO_AM_I register


!!! danger "Questions "
     Once you finished the code, show it to the teacher

### Reading the temperature from the sensor

In this step you will use the I2C bus to read the raw temperaturefrom the sensor, that is stored in its WHO_AM_I register

### Reading the temperature in celsius (optional)

This assignment is optional, but required if you want to obtain more than 6 / 10 in this assignment. 

Use the calibration mechanism to obtain the real value of temperature.

!!! note "Homework (Optional)"
	Once finished, the *Speaker* will contact me to **explain (orally) the code developed**
	






