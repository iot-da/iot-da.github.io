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

