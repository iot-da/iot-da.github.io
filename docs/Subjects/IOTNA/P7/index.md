# Final programming project

The final development (programming) project will be finally carried on **in teams of 2 people**.

## Project description 

The project must provide the following features:

* It must periodically  monitor   two I2C sensors of the ESP32-MeshKit-Sense board,  the temperature sensor (HTS221) and the ambient light sensor (BH1750FVI).  You will read the temperature sensor every 5 seconds and the light sensor every 2 seconds. 
* The *power manager* will be configured to enter light sleep whenever possible.
* There will be a LOG (level INFO) every 10 seconds informing of the last temperature and ambient light (illuminance, measured in lux) readings
* LED IO12 should be blinking every second to inform that the system is running. 
* If the ambient light sensor lux lecture goes below a certain threshold (decided by you), the LED IO2 will be on and LED IO12 will go off. 
* If the ambient light sensor readings remain under the threshold for more than 10 minutes, the system will enter deep sleep for 30 minutes.


### Optional parts

OPTIONALLY you could include all/some of the  following features:

* Design the system using the Finite State Machine (FSM) presented in the lectures.
* Instead of informing of the last temperature/illuminance reading, log the average of the readings since the last log.
* Before entering deep sleep, the system will write the current temperature and luminance reading in Flash, using the NVS partition. After waking up, and only if we are returning from a deep sleep,  there will be a LOG message informing of the stored temperature and illuminance before starting to read the sensors again.
* LED IO12 could be controlled using a PWM signal so its intensity changes depending on the current illuminance: if the illuminance is high, the LED IO12 will bright more. When the illuminance is less, the LED IO12 will be dimmer. You can check the [ESP-IDF documentation and examples for PWM](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/mcpwm.html) (in the documentation, PWM is used to control motors and servomotors. But the same signal could drive the LED, controlling its intensity).

## Important dates

* *Group notifications*. Remember that this assignment has to be done in a team of 2 people, so the **current groups are no longer valid**. Please send an email to Prof. Jose Ignacio him about your team for this project **before 29th Dec 2021**
* During the week of 10th January 2022, you will be able to work on this project during IOTNA lectures. You will be able to ask your questions to the Professor during those sessions. 
* *DEADLINE*: 24th January 2022.

### Delivery instructions
You must send your code (.c and .h files) to Prof. Jose Ignacio by email (jigomez@ucm.es) before the deadline expires.




 
 