import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import numpy as np
import cv2
currentexpression = 0
NeutralEyes = cv2.VideoCapture('Neutral Eyes.mp4')
AggressiveEyes = cv2.VideoCapture('Aggressive Eyes.mp4')
SleepingEyes = cv2.VideoCapture('Sleeping Eyes.mp4')
CryingEyes = cv2.VideoCapture('Crying Eyes.mp4')
CheerfulEyes = cv2.VideoCapture('Cheerful Eyes.mp4')
EmbarrasedEyes = cv2.VideoCapture('Embarrassed Eyes.mp4')
QuestionMarkEyes = cv2.VideoCapture('QuestionMark Eyes.mp4')
ShockedEyes = cv2.VideoCapture('Shocked Eyes.mp4')
SillyEyes = cv2.VideoCapture('Silly Eyes.mp4')
HeartEyes = cv2.VideoCapture('Heart Eyes.mp4')
HypnoticEyes = cv2.VideoCapture('Hypnotic Eyes.mp4')

def GraphicsDraw(video, file):
    if (video.isOpened()):
        ret, frame = video.read()
        if ret:
            cv2.imshow("Eye", frame)
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cv2.waitKey(15)
    else:
        video.open(file)
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        if "Eye" in window.get_name():
            window.maximize()
        elif "Terminal" in window.get_name():
            window.minimize()

def GraphicsClose(video):
    video.release()
    cv2.destroyAllWindows()

def GraphicsRefresh(ExpressionState):
    global currentexpression
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
    if currentexpression != ExpressionState:
        if currentexpression == 0:
            GraphicsClose(NeutralEyes)
        elif currentexpression == 1:
            GraphicsClose(AggressiveEyes)
        elif currentexpression == 2:
            GraphicsClose(SleepingEyes)
        elif currentexpression == 3:
            GraphicsClose(CryingEyes)
        elif currentexpression == 4:
            GraphicsClose(CheerfulEyes)
        elif currentexpression == 5:
            GraphicsClose(EmbarrasedEyes)
        elif currentexpression == 6:
            GraphicsClose(QuestionMarkEyes)
        elif currentexpression == 7:
            GraphicsClose(ShockedEyes)
        elif currentexpression == 8:
            GraphicsClose(SillyEyes)
        elif currentexpression == 9:
            GraphicsClose(HeartEyes)
        elif currentexpression == 10:
            GraphicsClose(HypnoticEyes)
    if ExpressionState==0:
        GraphicsDraw(NeutralEyes, 'Neutral Eyes.mp4')
    elif ExpressionState==1:
        GraphicsDraw(AggressiveEyes, 'Aggressive Eyes.mp4')
    elif ExpressionState==2:
        GraphicsDraw(SleepingEyes, 'Sleeping Eyes.mp4')
    elif ExpressionState==3:
        GraphicsDraw(CryingEyes, 'Crying Eyes.mp4')
    elif ExpressionState==4:
        GraphicsDraw(CheerfulEyes, 'Cheerful Eyes.mp4')
    elif ExpressionState==5:
        GraphicsDraw(EmbarrasedEyes, 'Embarrassed Eyes.mp4')
    elif ExpressionState==6:
        GraphicsDraw(QuestionMarkEyes, 'QuestionMark Eyes.mp4')
    elif ExpressionState==7:
        GraphicsDraw(ShockedEyes, 'Shocked Eyes.mp4')
    elif ExpressionState==8:
        GraphicsDraw(SillyEyes, 'Silly Eyes.mp4')
    elif ExpressionState==9:
        GraphicsDraw(HeartEyes, 'Heart Eyes.mp4')
    elif ExpressionState==10:
        GraphicsDraw(HypnoticEyes, 'Hypnotic Eyes.mp4')
    currentexpression = ExpressionState