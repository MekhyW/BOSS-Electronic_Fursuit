import serial
import numpy as np
import cv2
ExpressionState = 0
currentframe = 0
NeutralEyes = cv2.VideoCapture('Neutral Eyes_Left.mp4')
AggressiveEyes = cv2.VideoCapture('Aggressive Eyes_Left.mp4')
SleepingEyes = cv2.VideoCapture('Sleeping Eyes_Left.mp4')
CryingEyes = cv2.VideoCapture('Crying Eyes_Left.mp4')
CheerfulEyes = cv2.VideoCapture('Cheerful Eyes_Left.mp4')
EmbarrasedEyes = cv2.VideoCapture('Embarrassed Eyes_Left.mp4')
QuestionMarkEyes = cv2.VideoCapture('QuestionMark Eyes_Left.mp4')
ShockedEyes = cv2.VideoCapture('Shocked Eyes_Left.mp4')
SillyEyes = cv2.VideoCapture('Silly Eyes_Left.mp4')
HeartEyes = cv2.VideoCapture('Heart Eyes_Left.mp4')
HypnoticEyes = cv2.VideoCapture('Hypnotic Eyes_Left.mp4')

def GraphicsDraw(video):
    global currentframe
    if (video.isOpened()):
        ret, frame = video.read()
        cv2.namedWindow("Eye", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Eye", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        if ret:
            cv2.imshow("Eye", frame)
            video.set(cv2.CAP_PROP_POS_FRAMES, currentframe)
            currentframe += 1
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            currentframe = 0
        cv2.waitKey(15)

def GraphicsRefresh(ExpressionState):
    global NeutralEyes
    global AggressiveEyes
    global SleepingEyes
    global CryingEyes
    global CheerfulEyes
    global EmbarrasedEyes
    global QuestionMarkEyes
    global ShockedEyes
    global SillyEyes
    global HeartEyes
    global HypnoticEyes
    if ExpressionState==0:
        GraphicsDraw(NeutralEyes)
    elif ExpressionState==1:
        GraphicsDraw(AggressiveEyes)
    elif ExpressionState==2:
        GraphicsDraw(SleepingEyes)
    elif ExpressionState==3:
        GraphicsDraw(CryingEyes)
    elif ExpressionState==4:
        GraphicsDraw(CheerfulEyes)
    elif ExpressionState==5:
        GraphicsDraw(EmbarrasedEyes)
    elif ExpressionState==6:
        GraphicsDraw(QuestionMarkEyes)
    elif ExpressionState==7:
        GraphicsDraw(ShockedEyes)
    elif ExpressionState==8:
        GraphicsDraw(SillyEyes)
    elif ExpressionState==9:
        GraphicsDraw(HeartEyes)
    elif ExpressionState==10:
        GraphicsDraw(HypnoticEyes)

while True:
    try:
        JETSON = serial.Serial('/dev/ttyS0', 9600)
        break
    except:
        print("failed")

while True:
    try:
        if(JETSON == None):
            JETSON = serial.Serial('/dev/ttyS0', 9600)
        line = JETSON.readline.decode()
        if line:
            while JETSON.in_waiting():
                print(JETSON.readline())
            line.split("-")
            ExpressionState = int(line[0])
            currentframe = int(line[1])
            GraphicsRefresh(ExpressionState)
        else:
            GraphicsRefresh(ExpressionState)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    except:
        print("failed")
        if(not(JETSON == None)):
            JETSON.close()
            JETSON = None