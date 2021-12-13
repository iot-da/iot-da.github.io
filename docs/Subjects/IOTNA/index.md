# IoT Node Architecture

## General information

This subject will cover several topics regarding embedded system programmings. Specifically, we will learn to develop IoT projects using [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html), a framework built onto [FreeRTOS](https://www.freertos.org/).  Some specific goals if this subject are:

* Get a global view of a safe application  development cycle.
* Meet the main components of an IoT device
* Learn basic components of Real Time Operating Systems (RTOS)
* Work with sensors and learn the most common interfaces

### Subject program and evaluation methodology

  [Program and evaluation](slides/intro.pdf)

## Professors

Jose Ignacio Gomez (jigomez@ucm.es) and Katzalin Olcoz  (katzalin@ucm.es )

## Work groups

[Here you can find the current work groups](groups.md)

## Personal paper project assignment

[Here you can find  description about this individual assignment](paperProject.md)

## Quizzes
All quizzes will be done in [this link](https://b.socrative.com/login/student/). The name of the room is IOTUCM.
You MUST enter your name to answer the quizzes.


## Schedule

|    Day      | Topic                    |  Lab instructions   |  Deliverable   |
|--------------|------------------------|-------------------------|-------------------|
| 20/10  | [Introduction: boards, SoC](slides/soc.pdf)  |  [C Exercises](ctutorial/index.md)   |  |
| 21/10  | ESP-IDF environment  | [Online DEMO](demo/index.md)  |          |
| 27/10  | ESP-IDF   			| [1. Starting ESP-IDF ](P1/index.md)              | |
| 28/10  | ESP32 Memory map              | [1. Starting ESP-IDF ](P1/index.md)              | |
|03/11  | [ESP-IDF Tasks Scheduler](slides/tasks.pdf)     | [2. Tasks: matrix multiply ](P2/index.md)              |  |
|04/11  | [ESP-IDF Tasks Scheduler](slides/tasks.pdf)  | [2. Tasks: matrix multiply ](P2/index.md)    |   |
|10/11  | [Events and task notifications](slides/events.pdf) | [2. Tasks: matrix multiply  ](P2/index.md)    |   |
|11/11  | [Input/Output](slides/IO.pdf) -  [Polling/Interrupts](slides/interrupts.pdf) -  [GPIO](slides/gpio.pdf)  | [3. Chronometer](P3/index.md)                | | 
|17/11  | [Timers](slides/timer.pdf)	| 				[3. Chronometer](P3/index.md)            |     |
|18/11  |  Event based programming  	  		     | [3. Chronometer](P3/index.md)            | Lab 2 deadline    |
|24/11  |  Event based programming. [NAND/NOR Flash](slides/storage.pdf)    |[3. Chronometer](P3/index.md) |   |
|25/11  | [File system](slides/partitions.pdf). [System Log](slides/logging.pdf)       	|[4. Log in flash](P4/index.md) | |
|01/12  | [Watchdog](slides/watchdog.pdf) | [4. Log in flash](P4/index.md) |  Lab 3 deadline |
|02/12  | [Sensors](slides/sensors.pdf). 	    | [4. Log in flash](P4/index.md)            |  |
|08/12  | NO LECTURE (non working day)  | Spain National Holiday    | |
|09/12  | [Serial buses: I2C, SPI, UART](slides/serial.pdf)	  | [4. Log in flash](P4/index.md)                   |   |
|15/12  | [QUIZZ](https://b.socrative.com/login/student/)  ESP-IDF I2C API		  | [5. Built-in sensors](P5/index.md)                |  Lab4 deadline |
|16/12  | Energy consumption           | [5. Built-in sensors](P5/index.md)         |   |
|22/12 | Powering the system           | [6. Energy modes](P6/index.md) | |
|23/12 | Firmware update                 | Personal Project definition.   |  Labs 5 and 6 deadline |
|12/01 | Personal project                  | [7. Final Project](P7/index.md) |   |
|13/01 | Personal project                  | [7. Final Project](P7/index.md) | |

*The final, personal project, will be due before 20th Jan. 2022*

