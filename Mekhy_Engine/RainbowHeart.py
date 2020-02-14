import serial
import time
import numpy
import pyalsaaudio
AORTA = serial.Serial('COM0', 115200)
CAROTID = serial.Serial('COM0', 115200)

def ArduinoRefresh(ExpressionState):
    AORTA.write(ExpressionState)
    time.sleep(0.05)
    AORTA.write(pyalsaaudio.Mixer().getvolume()+20)
    CAROTID.write(ExpressionState)