from Expression import *
import TelegramBot
import VoiceMod
import Displays
import SoundEffects
import serial
ExpressionState = 1

while True:
    try:
        if(AORTA == None):
            AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        if(CAROTID == None):
            CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        if(RASPI == None):
            RASPI = serial.Serial('/dev/ttyTHS1', 9600)
        break
    except:
        print("failed")

while True:
    try:
        if(AORTA == None):
            AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        if(CAROTID == None):
            CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        if(RASPI == None):
            RASPI = serial.Serial('/dev/ttyTHS1', 9600)
        global volume
        Displays.GraphicsRefresh(ExpressionState)
        AORTA.write("{}\n".format(ExpressionState).encode())
        CAROTID.write("{}\n".format(ExpressionState).encode())
        RASPI.write("{}-{}\n".format(ExpressionState, Displays.currentframe).encode())
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

