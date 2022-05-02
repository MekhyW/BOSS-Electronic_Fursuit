import numpy as np
import cv2
import time
cap = cv2.VideoCapture('DEMO.mp4')
cap2 = cv2.VideoCapture('DEMO2.mp4')
t0 = time.time()

def GraphicsDraw(video):
    if (video.isOpened()):
        ret, frame = video.read()
        cv2.namedWindow("Eye", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Eye", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        if ret:
            cv2.imshow("Eye", frame)
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 500)
        cv2.waitKey(15)
        print(video.get(cv2.CAP_PROP_POS_FRAMES))

def GraphicsRefresh():
    global cap
    global cap2
    if(time.time() - t0 < 10):
        GraphicsDraw(cap)
    else:
        GraphicsDraw(cap2)

while True:
    GraphicsRefresh()