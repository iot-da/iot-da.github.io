# Reading sensors using I2C

## Goals

* Learn to use the API provided by ESP-IDF for the I2C serial buses
* Read the temperature from sensor HTS221 in the board

## Documentation

To complete this assignment, you may need to check the slides discussed in the lectures and the official API documentation:

* [ESP-IDF API for I2C](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html)
* [HTS221 sensor data sheet](https://www.st.com/resource/en/datasheet/hts221.pdf)
* [SoC reference](https://docs.espressif.com/projects/espressif-esp-iot-solution/en/latest/hw-reference/ESP32-MeshKit-Sense_guide.html)

## Reading the temperature sensor

### Obtaining information about the sensor

Using the data sheet, search the infomation required to read the sensor using I2C bus: slave address, addresses of the control registers, number of bytes needed to read the temperature.
Using the information from the SoC and the pin numbers writen in  the lower side of the board, find the information about: gpio pins connected to SDA, SCL and to the sensors VDD.
Using the API reference, find how to perform a write and a read through I2C.



!!! danger "Questions"
     All previous exercises **must be finished DURING the lecture (not afterwards)** and shown to the teacher during the Zoom meeting. 

### Reading the device identification

In this step you will use the I2C bus to read the device identificación of the temperature sensor, that is stored in its WHO_AM_I register.
Note that you must write a 0 in the GPIO pin that controls the VDD signal of the sensors. If not, the sensors will be in power-off state.

!!! danger "Stop and sycn "
     Once you finished the code, show it to the teacher

### Reading the temperature from the sensor

In this step you will use the I2C bus to read the raw temperature from the sensor.

!!! danger "Stop and sycn "
     Once you finished the code, show it to the teacher

### Reading the temperature in celsius (optional)

This assignment is optional, but required if you want to obtain more than 6 / 10 in this assignment. 

Use the calibration mechanism to obtain the real value of temperature.

!!! note "Homework (Optional)"
	Once finished, the *Speaker* will contact me to **explain (orally) the code developed**
	






