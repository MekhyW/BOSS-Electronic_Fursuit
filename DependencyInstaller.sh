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
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

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

#32-BIT KERNEL
sudo nano /boot/config.txt
# Add the following line at the end of the file: arm_64bit=0
reboot

# OPENCV
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.1.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.1.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.1.1 opencv
mv opencv_contrib-4.1.1 opencv_contrib
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D BUILD_EXAMPLES=OFF ..
make -j4
sudo make install
sudo ldconfig
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=2048 to CONF_SWAPSIZE=100
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

# AUTOSTART
chmod 755 launcher.sh
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add the following line before @xscreensaver: @lxterminal -e sh /home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/launcher.sh >/home/pi/BOSS-Electronic_Fursuit/Mekhy_Engine/logs/cronlog 2>&1
cd ..

# SETUP
# - set auto login and password for pi user
# - setup VNC connection for 4g hotspot (remember to try both 2.4GHz and 5GHz when tethering)
# - setup dual display scheme
# - disable screen blanking
# - insert credentials into Mekhy_Engine/resources/credentials.json
# - set app bar to hide when unused (with hidden size of 0)
# - enable CSI camera