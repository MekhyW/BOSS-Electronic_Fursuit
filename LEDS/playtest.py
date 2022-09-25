import cv2
import os, random
import time

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
target = random.choice([n for n in os.listdir() if n.startswith('fx')])
target = 'fx12.mp4'
cap = cv2.VideoCapture(target)
cap.set(cv2.CAP_PROP_FPS, 10)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (16, 16))
    if not ret:
        break
    cv2.imshow("window", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.02)