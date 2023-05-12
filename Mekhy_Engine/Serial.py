import serial
import time
ser_actuators = None
ser_leds = None

def convertExpressionStringToNumber(expression):
    if expression == "Neutral":
        return 0
    elif expression == "Angry":
        return 1
    elif expression == "Disgusted":
        return 2
    elif expression == "Sad":
        return 3
    elif expression == "Happy":
        return 4
    elif expression == "Scared" or expression == "Shocked":
        return 5
    elif expression == "Heart":
        return 6
    elif expression == "Hypnotic":
        return 7
    elif expression == "Sexy":
        return 8
    elif expression == "Demonic":
        return 9
    else:
        return 0
    
def convertStatuscodeStringToNumber(statuscode):
    if statuscode == 'Ok':
        return 0
    elif statuscode == 'Assistant listening':
        return 10
    elif statuscode == 'Assistant processing':
        return 11
    elif statuscode == 'Assistant responding':
        return 12
    elif statuscode == 'Message received':
        return 13
    elif statuscode == 'Processing media':
        return 14
    else:
        return 0
    
def serialConnect():
    global ser_actuators, ser_leds
    connected = False
    while not connected:
        try:
            ser_actuators = serial.Serial('/dev/ttyUSB0', 9600)
            ser_leds = serial.Serial('/dev/ttyACM0', 9600)
            connected = True
        except Exception as e:
            print(e)
            time.sleep(1)

def serialSendActuators(expression):
    ser_actuators.write(str(expression).encode() + b'\n')

def serialSendLeds(expression):
    ser_leds.write(str(expression).encode() + b'\n')
    print("Sent: " + str(expression).encode() + '\n')