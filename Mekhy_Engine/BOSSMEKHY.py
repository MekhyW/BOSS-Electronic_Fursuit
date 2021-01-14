import VoiceMod
import Displays
import SoundEffects
import HotwordActivator
import TelegramBot
import serial
import time
import numpy
import sounddevice
import struct
import sys
volume = 0
AORTA = None
CAROTID = None
RASPI = None

while True:
    try:
        AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        RASPI = serial.Serial('/dev/ttyTHS1', 9600)
        break
    except:
        print("failed")

def MainLoop(indata, outdata, frames, time, status):
    try:
        if(AORTA == None):
            AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        if(CAROTID == None):
            CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        if(RASPI == None):
            RASPI = serial.Serial('/dev/ttyTHS1', 9600)
        global volume
        volume = int((numpy.linalg.norm(indata)*6.375*0.5) + (volume*0.5))
        Displays.GraphicsRefresh(HotwordActivator.ExpressionState)
        AORTA.write("{}-{}\n".format(HotwordActivator.ExpressionState, volume).encode())
        CAROTID.write("{}-{}\n".format(HotwordActivator.ExpressionState, volume).encode())
        RASPI.write("{}-{}\n".format(HotwordActivator.ExpressionState, Displays.currenttime).encode())
    except:
        print("failed")
        if(not(AORTA == None)):
            AORTA.close()
            AORTA = None
        if(not(CAROTID == None)):
            CAROTID.close()
            CAROTID = None
        if(not(RASPI == None)):
            RASPI.close()
            RASPI = None

with sounddevice.Stream(callback=MainLoop):
    HotwordActivator.StartDetector(sys.argv[1:])
    sounddevice.sleep(99999)