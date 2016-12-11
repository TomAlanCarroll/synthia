# Welcome Home with Synthia

*Authors: [Geoff Khorn](https://github.com/gkhorn978), [Sarah Carroll](https://github.com/sarahes), and [Tom Carroll](https://github.com/TomAlanCarroll)*

Synthia is a Synthetic Intelligent Assistant for your home.

We love to give our homes unique personality with furniture, decor and lighting. But what if we could take that personalization futher and interact with our homes?

Synthia is an intelligent assistant that sends you off in the morning with helpful reminders, then welcomes you home at the end of each day. This is done using motion detection triggered by a camera built into a Raspberry Pi. If motion is detected within a certain time range in the morning or evening, it will trigger functions to play a customized message.

Synthia is written in Python 2.7.

## Prerequisites
1. Raspberry Pi 3 Model B with Raspbian Jessie
1. Pi NoIR camera
1. Bluetooth speaker (or 3.5mm powered speaker)
<div align="center">![Raspberry Pi and Speaker](synthia.jpg)</div>

## Setup
1. Install Python 2.7 on Raspberry Pi
1. Install OpenCV on the Raspberry Pi with [OpenCV-for-Pi](https://github.com/jabelone/OpenCV-for-Pi) (or if you want to compile OpenCV on the Pi: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3)
1. Install `virtualenv` for Python if you have not already done so.
1. Run the following commands to setup `virtualenv` within this repository folder on the Raspberry Pi:
    ```bash
    # Setup virtualenv and install pip modules:
    virtualenv --no-site-packages synthia-virtualenv
    source synthia-virtualenv/bin/activate
    pip install -r requirements.txt
    
    # A symlink is needed to use cv2 in Python:
    # NOTE: The directory of cv2.so may be different depending on how you installed OpenCV
    ln -s ~/.virtualenvs/cv/lib/python2.7/site-packages/cv2.so synthia-virtualenv/local/lib/python2.7/site-packages/cv2.so
    ```
1. Install `mpg321` on the Rasperry Pi
    ```bash
    sudo apt-get install mpg321
    ```
1. Configure the desired audio output device as the system's default on the Raspberry Pi
