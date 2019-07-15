#!/usr/bin/env bash

# Install snips
sudo apt-get update
sudo apt-get install -y dirmngr
sudo bash -c 'echo "deb https://raspbian.snips.ai/$(lsb_release -cs) stable main" > /etc/apt/sources.list.d/snips.list'
# if the following command fails try a different keyserver such as hkp://pgp.mit.edu:80
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D4F50CDCA10A2849
sudo apt-get update
sudo apt-get install -y snips-platform-voice
sudo apt-get install -y snips-template snips-skill-server
sudo apt-get install -y snips-watch
sudo cp asound.conf /etc

# Configure the speaker & USB microphone with alsamixer
alsamixer

# Restart the audio server
sudo systemctl stop snips-audio-server
sudo systemctl start snips-audio-server

# Install npm


#sudo apt-get install python-dev python-all-dev libjpeg-dev vlc libffi-dev libssl-dev flac

# Install pip modules (this could take a while):
# pip install -r requirements.txt

# Install OpenCV in virtualenv (OpenCV-for-Pi does not work in virtualenv by default)
#wget "https://github.com/jabelone/OpenCV-for-Pi/raw/master/latest-OpenCV.deb"
#dpkg -x latest-OpenCV.deb ./OpenCV
#cp OpenCV/usr/local/lib/python2.7/dist-packages/cv2.so synthia-virtualenv/local/lib/python2.7/site-packages/
#rm latest-OpenCV.deb