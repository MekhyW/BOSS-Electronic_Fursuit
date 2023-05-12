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
sudo apt-get install -y git-lfs
sudo apt-get install -y python3-pip
sudo apt install -y ffmpeg
sudo apt install -y sox
sudo apt install -y python3-gi gir1.2-wnck-3.0
sudo apt install -y libsdl2-mixer-2.0-0
sudo apt install -y arduino
# PIP PACKAGES
sudo pip3 install --upgrade pip
sudo pip3 install telepota
sudo pip3 install googletrans==3.1.0a0
sudo pip3 install opencv-python
sudo pip3 install picamera[array]
sudo pip3 install scikit-learn
sudo pip3 install pygame --upgrade
sudo pip3 install pytube
sudo pip3 install gTTS
sudo pip3 install mediapipe-rpi4
sudo pip3 install openai
sudo pip3 install pvporcupine
sudo pip3 install pvrecorder
sudo pip3 install pyserial
sudo pip3 uninstall protobuf
sudo pip3 install protobuf==4.21.10
#EMOTION RECOG MODEL
cd Mekhy_Engine/resources
git lfs pull
cd ..
# AUTOSTART
chmod 755 launcher.sh
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add the following line before @xscreensaver: @lxterminal -e sh /home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/launcher.sh >/home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/logs/cronlog 2>&1
cd ..
#OVERCLOCK
sudo nano /boot/config.txt
# Change the following lines:
# over_voltage=2
# arm_freq=1700
cd ..
# SETUP
# - set auto login and password for pi user
# - setup VNC connection for 4g hotspot (remember to use 5GHz!!, 2.4GHz is too slow to work)
# - setup dual display scheme
# - insert credentials into Mekhy_Engine/resources/credentials.json
# - set app bar width to zero
# - enable CSI camera