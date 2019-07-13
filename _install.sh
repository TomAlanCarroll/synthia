#!/usr/bin/env bash

#sudo apt-get install python-dev python-all-dev libjpeg-dev vlc libffi-dev libssl-dev flac

# Setup virtualenv (change directory to repository directory if you haven't already)
pip install virtualenv
virtualenv --no-site-packages venv
source venv/bin/activate

# Install pip modules (this could take a while):
pip install -r requirements.txt

# Install OpenCV in virtualenv (OpenCV-for-Pi does not work in virtualenv by default)
#wget "https://github.com/jabelone/OpenCV-for-Pi/raw/master/latest-OpenCV.deb"
#dpkg -x latest-OpenCV.deb ./OpenCV
#cp OpenCV/usr/local/lib/python2.7/dist-packages/cv2.so synthia-virtualenv/local/lib/python2.7/site-packages/
#rm latest-OpenCV.deb