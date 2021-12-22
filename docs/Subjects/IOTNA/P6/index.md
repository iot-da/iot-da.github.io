# Lab 6. Energy saving modes

## Goals
Learn the mechanisms provided by ESP-IDF to exploit the different energy modes existing in ESP32 SoCs:

* Explicit moving into *light sleep* and *deep sleep* modes
* Discover wakeup reasons.
* Configuring and using the automatic power manager in ESP-IDF.

## Documentation

To complete this assignment, you may need to check the slides discuss in the lectures and the official API documentation:

* [Sleep modes](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html)
* [Power manager](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/power_management.html)

It is also relevant to check the examples provided in GitHub:

* [Light sleep](https://github.com/espressif/esp-idf/tree/master/examples/system/light_sleep)
* [Deep sleep](https://github.com/espressif/esp-idf/tree/master/examples/system/deep_sleep)
* [Wifi Power save](https://github.com/espressif/esp-idf/tree/master/examples/wifi/power_save)


## Explicitly moving to low power modes

We will start from a basic code monitoring any input device (like the button or the temperature sensor), where the main program is in an endless loop reading, periodically, the device status. The structure of the starting code could be similar to:

```c
while (1) {
    med = read_device(); // Could be button, sensor...
    ESP_LOGI(TAG,"Medida: %f", med);
    vTaskDelay(pdMS_TO_TICKS(DELAY));
}
```

Implement the following modifications:

* Include a explicit call to enter *light sleep* after 5 iterations. Previously, you will configure the *wakeup* mechanism to be the *timer* and instruct it to wake the system up after 10 seconds.
* Repeat the previous point but entering *deep sleep*
* Include code to determine the cause of the *wakeup* for both previous cases.


!!! danger  "Questions"
	* What difference do you observe when entering *deep sleep* compared with *light sleep*? What does it happen after 10 seconds in each case?
	* Where do you need to include the code to determine the *wakeup* cause in each of the two cases?


## Using the Power Manager

Starting from the same simple code of previous section, we will be using the *Power Manager* provided by ESP-IDF. 

In order to do so, we must enable *Dynamic frequency scaling* (DFS). We can enable it with *menuconfig* -> *Component config -> Power Management -> Support for Power Management -> Enable DFS at startup*.  It is also possible to configure it in our own code using the call `esp_pm_configure()`. 

You will use this latter method (`esp_pm_configure()`) and define:
* Max. frequency of 240MHz
* Min. frequency of 40MHz
* Enable automatic entering *light sleep mode*

To enable automatic entering *light sleep mode* we must activate the corresponding option in *menuconfig*:  *Component config -> FreeRTOS -> Tickless Idle Support* (this option is only visible if the *Enable DFS at startup* option is also enabled).

Following the earlier pseudo-code, modify your code in order to guess the *wakeup* cause. The structure of code could be now similar to:


```c
while (1) {
    med = read_device(); // Could be button, sensor...
    ESP_LOGI(TAG,"Medida: %f", med);
    vTaskDelay(pdMS_TO_TICKS(DELAY));
    cause =  get_wakeup_cause();
}
```
!!! danger  "Questions"
	* Which mechanism is waking the system up when using the *Power Manager*?

## Using High Resolution Timers (OPTIONAL)

Modify your code to monitor the device (sensor, button...) using a *High Resolution Timer* instead of using the call to `vTaskDelay(pdMS_TO_TICKS(DELAY))`.  The main task will configure the high resolution timer and then go to sleep for 100 seconds in and endless loop.

### Entering light sleep mode manually

 Modify your code to enter *light sleep mode* (calling  `esp_light_sleep_start()`)   after 3 executions of the *high resolution timer* callback. Set the high resolution timer to trigger every 3 seconds, and program the system to wake up after 10 seconds. Include a log message in the callback function which prints the number of times the callback function has been called.

!!! danger  "Questions"
	* Call  `esp_light_sleep_start()` outside the callback function of the high resolution timer.  What happens when the system wakes up? Are there log messages lost? Do they happen when they should happen?
	* No call  `esp_light_sleep_start()` inside the callback function of the high resolution timer. Do you observe any difference?
	
### Automatically entering light sleep mode

Repeat previous experiments using the Power Manager. 

!!! danger  "Questions"
	* Note that, since you do not manually enter the sleep mode, you will not move into *light sleep* after 3 executions of the high resolution timer. When is the system moving to *light sleep*?
	* What happens with the callback log messages? Do they happen when they should happen?


## Delivering the assignment
Once you finish the complete assignment (at least the first two sections), please send an email to Prof. Jose Ignacio (jigomez@ucm.es) with the codes develop for each section and a text file (text or PDF) with your answers to the questions. Please send only one email per group.

**DEADLINE: 12th January 2022**

