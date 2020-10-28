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
AORTA = serial.Serial('/dev/ttyUSB0', 9600)
CAROTID = serial.Serial('/dev/ttyUSB2', 9600)
RASPI = serial.Serial('/dev/ttyUSB1', 9600)

def MainLoop(indata, outdata, frames, time, status):
    global volume
    volume = (numpy.linalg.norm(indata)*6.375*0.5) + (volume*0.5)
    volume = int(volume)
    print(volume)
    Displays.GraphicsRefresh(HotwordActivator.ExpressionState)
    AORTA.write("{}-{}\n".format(HotwordActivator.ExpressionState, volume).encode())
    CAROTID.write("{}\n".format(HotwordActivator.ExpressionState).encode())
    RASPI.write("{}-{}\n".format(HotwordActivator.ExpressionState, Displays.currentframe).encode())

with sounddevice.Stream(callback=MainLoop):
    HotwordActivator.StartDetector(sys.argv[1:])
    sounddevice.sleep(99999)