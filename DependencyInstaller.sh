#!/bin/sh
#
# This script will install all the dependencies for the project.
#
# Usage:
# ./DependencyInstaller.sh
#
# This is made for Raspberry Pi 4 running Raspbian Buster.
#
# -----------------------------------------------------------------------------
sudo apt-get update
sudo apt-get install -y git-all
sudo apt-get install -y python3-pip
sudo apt install -y ffmpeg
sudo apt install -y sox
sudo apt install -y python3-gi gir1.2-wnck-3.0
sudo apt install -y libsdl2-mixer-2.0-0
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y python3-dev
# PIP PACKAGES
pip3 install --upgrade pip
pip3 install telepota
pip3 install googletrans==3.1.0a0
pip3 install opencv-python
pip3 install picamera[array]
pip3 install pygame --upgrade
pip3 install pytube
pip3 install gTTS
pip3 install mediapipe-rpi4
pip3 install openai
pip3 install pvporcupine
pip3 install pvrecorder
pip3 install pyserial
# -----------------------------------------------------------------------------
#
# Remember to:
# - set auto login and password for pi user
# - setup new VNC address
# - setup dual display scheme
# - insert credentials into Mekhy_Engine/resources/credentials.json
# - run sudo nano /etc/rc.local and add the following line before exit 0: "python3 /home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/BOSSMEKHY.py &"
# - set app bar width to zero
# - enable CSI camera