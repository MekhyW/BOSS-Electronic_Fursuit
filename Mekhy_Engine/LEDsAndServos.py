import serial
import time
import numpy
import pyaudio
import struct
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)
AORTA = serial.Serial('COM0', 9600)
CAROTID = serial.Serial('COM0', 9600)

def GetVolume():
    data = stream.read(1024)
    data_int = struct.unpack(str(2048) + 'B', data)
    return data_int[0]

def ArduinoRefresh(ExpressionState):
    AORTA.write("{}-{}\n".format(ExpressionState, GetVolume()).encode())
    CAROTID.write("{}\n".format(ExpressionState).encode())