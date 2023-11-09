#!/bin/sh
#
# This script will install all the dependencies for the project.
#
# Usage:
# ./DependencyInstaller.sh
#
# This is made for Raspberry Pi 4 running Raspbian Buster (Raspberry Pi OS Legacy, 05/03/2023 build).
#
# -----------------------------------------------------------------------------
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y cmake
sudo apt-get install -y python3-pip
sudo apt install -y ffmpeg
sudo apt install -y sox
sudo apt install -y python3-gi gir1.2-wnck-3.0
sudo apt install -y libsdl2-mixer-2.0-0
sudo apt install -y arduino
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libfontconfig1-dev libcairo2-dev
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install xdotool

# PIP PACKAGES
sudo pip3 install --upgrade pip
sudo pip3 install telepota==1.0
sudo pip3 install googletrans==3.1.0a0
sudo pip3 install numpy==1.21.6 
sudo pip3 install picamera[array]==1.13
sudo pip3 install pygame --upgrade
sudo pip3 install spotdl==4.2.0
pip3 install --upgrade typing_extensions
sudo pip3 install gTTS==2.3.2
sudo pip3 install mediapipe-rpi4==0.8.8
sudo pip3 install openai==0.27.8
sudo pip3 install pvporcupine==2.1.4
sudo pip3 install pvrecorder==1.1.1
sudo pip3 install pyserial==3.4
sudo pip3 uninstall protobuf
sudo pip3 install protobuf==4.21.10
sudo pip3 install pyautogui==0.9.54
sudo pip3 install python-vlc

# AUTOSTART
chmod 755 launcher.sh
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add the following line before @xscreensaver: @lxterminal -e sh /home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/launcher.sh >/home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/logs/cronlog 2>&1
cd ..

# SETUP
# - set auto login and password for pi user
# - setup VNC connection for 4g hotspot (always tether by USB. When running, if the bot fails to connect to the internet, close and reopen the usb tether connection)
# - setup dual display scheme, make sure that the left display is the primary display (so that the eyes are extended to the right display)
# - set taskbar to autohide
# - disable screen blanking
# - insert credentials into Mekhy_Engine/resources/credentials.json
# - enable CSI camera