# Basic Input/output in ESP-IDF

## Goals

* Learn the basics of input/output, using polling and interrupts
* Configuring and use GPIO pins as input/output
* Program *timers* to schedule periodic events

## Documentation

To complete this assignment, you may need to check the slides discuss in the lectures and the official API documentation:

* [GPIO](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html)
* [Timers](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_timer.html)

## Using GPIO

### Checking connections

The first step when using external peripherals connected to our SoC (ESP32) is to learn how are they connected. The module exposes a series of pines from the core and the operating system (ESP-IDF) assigns them a number. We need then to find out which pin number correspond to every relevant connection to us.

In this fist step, you must find out the GPIO number for the button and LED.  The information is usually included in the documentation of the SoC and the board: we need to check both, the SoC and the board. In our case, part of the information may be found in the brief [online documentation](https://docs.espressif.com/projects/espressif-esp-iot-solution/en/latest/hw-reference/ESP32-MeshKit-Sense_guide.html).	 If you don't find all the information there, try to look it up carefully in the board itself. Sometimes, this information is printed on the PCB...



### Simple GPIO polling: button

The next step will be to set up the button to use it as an input for our system. First, you will need to configure the GPIO pin:

* Configure the pin as INPUT.
* Disable interrupts.
* Enable pull-ip mode.

Check the slides and documentation to learn how to do this configuration in ESP-IDF. Remember that you need to declare a variable of type `gpio_config_t`, assign the relevant fields of such variable and finally call `gpio_config( )`  to complete the configuration.

Once the configuration of the GPIO is done, you can write a simple sampling loop. Write and endless *while* loop where you poll the status of the button, print a message if the button is pressed and wait for 250ms before polling again. A **pseudo-code** for such loop could be the following:

```c
while (1) {
   int status = gpio_get_level(GPIO_BUTTON_PIN);
   if (status == BUTTON_PRESSED)
      printf("Button pressed!!\n");
   delay(250);
}
```


### GPIO input and output: button + LED

In the next step, you will configure a GPIO pin as an output in order to control the LEDs.  Similar to the button configuration, the first step is to configure the respective pins (there are two LEDs available):

* Configure the pin(s) as OUTPUT.
* Disable interrupts.
* Disable pull-up and pull-down modes.

Remember to use  a variable of type `gpio_config_t` and complete the configuration with a call to `gpio_config( )`.

Once both the three pins (one input, two outputs) are correctly configured, you will develop a very simple program that will switch one of the LEDs (on/off) every time the 
button is pressed. The *pseudo-code* may be similar to:

```c
while (1) {
   int status = gpio_get_level(GPIO_BUTTON_PIN);
   if (status == BUTTON_PRESSED) {
    	if LED_IS_ON 
	   gpio_set_level(GPIO_LED_PIN, OFF);
	else
           gpio_set_level(GPIO_LED_PIN, ON);
   }
	   
    delay(250);
}
```

!!! danger "Stop and sync "
	Please send a message in Zoom chat  to the professor as soon as you finished
	
	
### GPIO interrupts

In this subsection you will change the polling mechanism and use interrupts instead. Starting from the configuration you already have for the button GPIO pin, you need to do certain modifications:

* Enable interrupts (for example, `POSEDGE`). You may change the edge/level later using `gpio_set_intr_type()`.
* Register the ISR that will be executed when the interrupt rises. You will need to call `gpio_install_isr_service()` and `gpio_isr_handler_add`.

Once the new configuration is done, you need to write the ISR for the button interrupts. Remember to use the correct protoype: `static void IRAM_ATTR gpio_isr_handler(void* arg)`(you may change the name of the ISR itself, but not its prototype).

Finally, adapt the previous code (LED switching) to work with the new code. How are you going to notify you main loop about a new interrupt?


### Extending button functionality
Just to play a bit longer with interrupts, let's extend the functionality of our application. Adapt your code so you can identify if the button was pressed *normally* or if it was hold at least for 4 seconds:

* If the button was just pressed (less than 4 seconds) you will switch the green LED.
* If the button was pressed and hold for more than 4 seconds, you will switch the red LED.

Note that, if both LEDs are on, you will see a yellow light.

!!! danger "Stop and sync "
      Please send a message (using Zoom) to the professor as soon as you finished.
	
## Timers

Now we will include timers in our design.  Read again the slides and [API documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_timer.html) to remember how to declare and configure a timer in ESP-IDF.

### LED blink

Then, create a timer that will blink the red LED every second (i.e. the red LED will be on for one second, then off for another second and so on). The green LED will still be controlled with the button (but keep your code detecting when the button was pressed for more than 4 seconds; you will use it later).

### Controlling blinking frequency

We will define several blinking periods: 500ms,  1s or 2s. When your program starts, the red LED will be blinking every 500ms.  Then, your code must do the following:

* When the button is pressed, the period will increase, first to 1 second, then to 2 seconds.
* If the button is pressed when the period is already 2 seconds, nothing changes.
* When the button is held pressed for more than 4 seconds, the period will decrease (from 2s to 1s and then to 500ms).
* If the button is held pressed for more than 4 seconds when the period is 500ms, nothing changes.


!!! danger "Stop and sync "
     All previous exercises **must be finished DURING the lecture (not afterwards)** and shown to the teacher during the Zoom meeting. AFTER they are shown to be working during the lecture, the *Recorder* of the group will send an email with the source code of the last section (*Controlling blinking frequency*). Remind that plagiarism is strictly prohibited: the code of each group must be solely developed by members of that group.

## Chronometer (optional)

This assignment is optional, but required if you want to obtain more than 6 / 10 in this assignment. You will need to implement a simple chronometer with the following functionality:

* The chronometer counts minutes and seconds.
* Pressing the button starts/stops counting.
* Holding pressed the button for more than 4 seconds resets the count to 0.
* Every second, the actual count (in a format MM:SS) will be shown in the terminal (using `printf()`).

!!! note "Homework (Optional)"
	Implement the chronometer using, at least, one *timer*. Once finished, the *Speaker* will contact me to **explain (orally) the code developed**
	







