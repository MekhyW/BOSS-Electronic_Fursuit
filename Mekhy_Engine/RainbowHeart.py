import serial
import time
import numpy
import pyalsaaudio
SAPHENOUS = serial.Serial('COM26', 115200)

def ArduinoRefresh(ExpressionState):
    SAPHENOUS.write(ExpressionState)
    time.sleep(0.01)
    SAPHENOUS.write(pyalsaaudio.Mixer().getvolume()+20)