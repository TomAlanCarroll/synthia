# Synthia
## The Synthetic Intelligent Assistant for your home.

Synthia is an intelligent assistant that sends you off in the morning with helpful reminders, then welcomes you home at the end of each day. This is done using motion detection triggered by a camera built into a Raspberry Pi. If motion is detected within a certain time range in the morning or evening, it will trigger functions to play a customized message.

## Hardware Prerequisites
1. Raspberry Pi 3 or 4 with Raspbian Strech
1. Pi NoIR camera
1. Bluetooth speaker (or 3.5mm powered speaker)

<div align="center">

![Raspberry Pi and Speaker](synthia.jpg)
</div>

## Setup
1. Configure the desired audio output device as the system's default on the Raspberry Pi
1. Set the correct timezone on the Raspberry Pi
1. Load this repository to /home/pi on the Raspberry Pi and run:
```bash
/home/pi/_install.sh
```

# How to Setup
Execute the following line on the Raspberry Pi:
```bash
# or with a custom config:
python synthia.py --config=my-config.json --user=<YOUR_NAME>
```
The default configuration is to each day execute exactly one morning event between 6:00 and 10:00  and exactly one welcome home event between 18:00 and 23:00. These times are relative to the current time on the Raspberry Pi.
