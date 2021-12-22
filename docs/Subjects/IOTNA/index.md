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

## Work groups (for regular lab assignments)

[Here you can find the current work groups](groups.md)

## Personal paper project assignment

[Here you can find  description about this individual assignment](paperProject.md)

## Final programming project (teams of 2 people)
[Here you can find  description about this  assignment](P7/index.md)


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
|15/12  | [QUIZ](https://b.socrative.com/login/student/).  [ESP-IDF I2C API](slides/i2c-idf.pdf)	  | [5. Built-in sensors](P5/index.md).   [HTS221 Datasheet](slides/hts221.pdf)               |  Lab4 deadline |
|16/12  |    I2C        | [5. Built-in sensors](P5/index.md) .  [HTS221 Datasheet](slides/hts221.pdf)      |   |
|22/12 | [Energy consumption](slides/energy.pdf). [Powering the system](slides/espPower.pdf)      | [5. Built-in sensors](P5/index.md) | |
|23/12 |  [QUIZ](https://b.socrative.com/login/student/). [ESP32 power modes](slides/lowpower.pdf)             | [6. Low power modes](P6/index.md)  |  Labs 5  deadline |
|12/01 | Final Programming project  (groups of 2)              | [7. Final Project](P7/index.md) |   Paper project deadline   |
|13/01 | Final Programming project                  | [7. Final Project](P7/index.md) |  Lab 6 deadline |

*The final programming project, will be due before 24th Jan. 2022*

