# Logging and flash filesystem

## Goals

* Learn the logging mechanisms provided by ESP-IDF
* Create your own partitions in SPI FLASH memory
* Mount a filesystem in FLASH memory

## Documentation

To complete this assignment, you may need to check the slides discuss in the lectures and the official API documentation:

* [Log](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/log.html)
* [SPI Flash and partitions](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/spi_flash.html)
* [FAT filesystem](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/fatfs.html)
* [Wear levelling API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/wear-levelling.html)

## Logging to UART

### Basic logging

Start from your basic (single-task) matrix multiply code (Lab 2). Insert `ESP_LOG` calls at least at 3 levels: ERROR, INFO and VERBOSE. 

### Modify logging level via menuconfig

Use `menuconfig` to select INFO as the minimum log level. Check that the VERBOSE messages are not shown


### Multimodule
Create a new .c file in your project. Include there a couple of functions from your code. Remind to declare. a new TAG there. Include LOG macros in both files. 
 
### Modify logging level at runtime
Use `esp_log_level_set()`to set WARNING as the log level for the main file and VERBOSE for the other file. Check that the log output is correct.


!!! danger "Stop and sync "
     All previous exercises **must be finished DURING the lecture (not afterwards)** and shown to the teacher during the Zoom meeting. AFTER they are shown to be working during the lecture, the *Recorder* of the group will send an email with the source code of the last section (*Modify logging level at runtime*). 
     Remind that plagiarism is strictly prohibited: the code of each group must be solely developed by members of that group.

## Mounting FAT filesystem

In this step you will mount a FAT filesystem in a new partition created in the SPI FLASH existing in the board. 
Follow the example *Wear Levelling* ( [wear levelling example])https://github.com/espressif/esp-idf/tree/master/examples/storage/wear_levelling) ) and create a PlatformIO project to run it in your board:

* Create the PlatformIO project and copy the source code from the *Wear Levelling* example.
* Copy the file `partitions_example.csv` in the root folder of your project. Rename it as `partitions.csv`
* Modify the file *platformio.ini* to include:
	* `monitor_port = /dev/ttyUSB1`
	* `upload_port = /dev/ttyUSB1`
	* `board_build.partitions = partitions.csv`
* Run *menuconfig* (type `pio run -t menuconfig` in a PlatformIO terminal)
	* *Partition Table* --> *PartitionTable* --> *Custom partition table CSV*
	* Check that the name of the *Custom parition CSV file* in *menuconfig* is *partitions.csv*
	* Save the new configuration (press `S`) and quit (press `Q`)

Build, upload and execute. Monitor the output and check that the messages are the ones expected.

!!! danger "Questions "
     Once you finished the code, try to answer the following questions. Include them in the report of this assignment.
     
     * What is the name of the file you are creating in this example?
     * What is the path of the file? Why? When was that *folder* created?
     * What is the difference between `printf()` and `fprintf()`
     * Why there are two calls to `fopen()? What is the difference between them?   
     * What is `fgets()`doing? 
     * Write a code that creates a new file called `timestamp.txt` whose content is a timestamp (time elapsed since boot). How can we later modify its content?
     * Try to open a file after the call èsp_vfs_fat_spiflash_umount()*. What happens?


## Redirecting the log to FLASH (optional)

This assignment is optional, but required if you want to obtain more than 6 / 10 in this assignment. 

Starting from your chronometer code (or equivalent), include LOG messages (using ESP_LOG macros) and redirect the log to a file called *log.txt* that you will create in a FAT partition in SPI FLAG. Use `esp_log_set_vprintf()` to do the redirection. You should LOG:

* Every 5 seconds of the chronometer running, you must LOG a message.
* Every time the button is pressed
* Every time there is a *long* press (more than 4 seconds).

Note that you can still use `printf()` to write to the terminal.

Also, after 1 minute of functioning, you will read the first 5 lines of the log file and write them to the terminal (using ` printf()`).

!!! note "Homework (Optional)"
	Once finished, the *Speaker* will contact me to **explain (orally) the code developed**
	






