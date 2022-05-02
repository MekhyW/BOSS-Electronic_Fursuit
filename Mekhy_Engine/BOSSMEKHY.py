import Expression
import TelegramBot
import VoiceMod
import Displays
import SoundEffects
import serial
AORTA = None
CAROTID = None

while True:
    try:
        if(AORTA == None):
            AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        if(CAROTID == None):
            CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        break
    except:
        print("failed")

while True:
    try:
        if(AORTA == None):
            AORTA = serial.Serial('/dev/ttyUSB0', 9600)
        if(CAROTID == None):
            CAROTID = serial.Serial('/dev/ttyUSB1', 9600)
        Displays.GraphicsRefresh(Expression.ExpressionState)
        AORTA.write("{}\n".format(Expression.ExpressionState).encode())
        CAROTID.write("{}\n".format(Expression.ExpressionState).encode())
    except:
        print("failed")
        if(not(AORTA == None)):
            AORTA.close()
            AORTA = None
        if(not(CAROTID == None)):
            CAROTID.close()
            CAROTID = None

