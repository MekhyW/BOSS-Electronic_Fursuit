#!/bin/sh
#
# This script will install all the dependencies for the project.
#
# Usage:
# ./DependencyInstaller.sh
#
# -----------------------------------------------------------------------------
sudo apt-get update
sudo apt-get install -y git-all
sudo apt-get install -y python3-pip
sudo apt install -y ffmpeg
sudo apt install -y sox
sudo apt-get install -y python3-pip
sudo apt install -y python3-gi gir1.2-wnck-3.0
# PIP PACKAGES
pip3 install --upgrade pip
pip3 install telepota
pip3 install googletrans==3.1.0a0
pip3 install opencv-python
pip3 install picamera[array]
pip3 install pygame
pip3 install pytube
pip3 install gTTS
pip3 install mediapipe-rpi4
pip3 install openai
pip3 install pvporcupine
pip3 install pvrecorder
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
# ROS
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu buster main" > /etc/apt/sources.list.d/ros-noetic.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt update
sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake
sudo rosdep init
rosdep update
mkdir ~/ros_catkin_ws
cd ~/ros_catkin_ws
rosinstall_generator ros_comm --rosdistro noetic --deps --wet-only --tar > noetic-ros_comm-wet.rosinstall
wstool init src noetic-ros_comm-wet.rosinstall
rosdep install -y --from-paths src --ignore-src --rosdistro noetic -r --os=debian:buster
sudo dphys-swapfile swapoff
sudoedit /etc/dphys-swapfile # Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
sudo src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/noetic -j1 -DPYTHON_EXECUTABLE=/usr/bin/python3
source /opt/ros/noetic/setup.bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
# -----------------------------------------------------------------------------
#
# Remember to:
# - set auto login and password for pi user
# - setup new VNC address
# - setup dual display scheme
# - insert telegram bot token into TelegramBot.py
# - run sudo nano /etc/rc.local and add the following line before exit 0: python3 ~/BOSS-Electronic_Fursuit/Mekhy_Engine/BOSSMEKHY.py