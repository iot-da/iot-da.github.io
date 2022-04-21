# Laboratory 1. IP Camera Pentest

## Introduction

The objective of this laboratory session is to put into practice the knowledge on how to carry out a penetration test (*pentest*) on a specific device, such as an IP camera. 

To carry out the laboratory we will need the following software elements:

1. IOTNA Ubuntu Virtual Machine ([Download & Instructions](../../IOTNA/demo/index.md))
2. IP Camera firmware:
    1. SPI extracted version ([spi_firmware.bin](spi_firmware.bin))
    2. Micro SD extracted version ([usd_firmware.zip](usd_firmware.zip))
3. [Binwalk](#binwalk)
4. [Ghidra](#ghidra)

### Binwalk

[Binwalk](https://github.com/ReFirmLabs/binwalk) is a fast, easy to use tool for analyzing, reverse engineering, and extracting firmware images.

Minimal installation instructions inside Ubuntu VM:
```bash
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
sudo python3 setup.py install
```
Dependencies:
```bash
# Install sasquatch to extract non-standard SquashFS images
sudo apt-get install zlib1g-dev liblzma-dev liblzo2-dev
git clone https://github.com/devttys0/sasquatch
(cd sasquatch && ./build.sh)

# Install jefferson to extract JFFS2 file systems
sudo apt-get install pip
sudo pip install cstruct
git clone https://github.com/sviehb/jefferson
(cd jefferson && sudo python3 setup.py install)

# Entropy study
sudo pip install matplotlib
```

### Ghidra

[Ghidra](https://github.com/NationalSecurityAgency/ghidra/releases): A Software Reverse Engineering (SRE) suite of tools developed by NSA's Research Directorate in support of the Cybersecurity mission.

Dependencies:

```bash
sudo apt-get install default-jre default-jdk
```

Download [Hidra 10.1.2](https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.1.2_build/ghidra_10.1.2_PUBLIC_20220125.zip), unzip and execute (`./ghidraRun`).

## Tasks

1. Download and import the IOTNA Ubuntu Virtual Machine available in the [link](https://iot-da.github.io/Subjects/IOTNA/demo/)

2. Follow the [tutorial](https://www.youtube.com/watch?v=fTGTnrgjuGA&ab_channel=stacksmashing) example:

   * Get the file from [easy_reverse](https://crackmes.one/crackme/5b8a37a433c5d45fc286ad83) (zip password: `crackmes.one`) or use directly the uncompressed file [rev50.zip](rev50.zip)

   - Obtain and test the password

3. Download the firmware `ip_cam_attify.bin` and use `binwalk` to extract its content.

4. Locate the `npc.tar.gz` and extract its content
5. Analyze the `npc` file with Ghidra:
    1. Execute `ghidra_10.1.2_PUBLIC/ghidraRun`
    2. Create a project, import the `npc` file and analyze it
    3. The camera rejects modified Firmwares with the message: `Md5 err!`
    4. Find the string and locate the functions in which it is used
