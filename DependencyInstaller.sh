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
sudo apt-get install libsdl2-mixer-2.0-0
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install python3-dev
sudo apt-get install xterm
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
# TENSORFLOW
mkdir tf_pi
cd tf_pi
sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev
python3 -m pip install keras --no-deps
python3 -m pip install keras_applications==1.0.8 --no-deps
python3 -m pip install keras_preprocessing==1.1.0 --no-deps
python3 -m pip install h5py==2.9.0
sudo apt-get install -y openmpi-bin libopenmpi-dev
sudo apt-get install -y libatlas-base-dev
python3 -m pip install -U six wheel mock
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.0.0/tensorflow-2.0.0-cp37-none-linux_armv7l.whl
python3 -m pip uninstall tensorflow
python3 -m pip install tensorflow-2.0.0-cp37-none-linux_armv7l.whl
cd ..
# -----------------------------------------------------------------------------
#
# Remember to:
# - set auto login and password for pi user
# - setup new VNC address
# - setup dual display scheme
# - insert credentials into Mekhy_Engine/resources/credentials.json
# - run sudo nano /etc/rc.local and add the following line before exit 0: "python3 /home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/BOSSMEKHY.py &"
# - set app bar size to minimum
# - enable CSI camera