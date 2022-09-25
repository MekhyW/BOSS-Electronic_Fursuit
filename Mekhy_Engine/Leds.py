import cv2
import numpy as np
import math, random, time
import os
LED_COUNT = 256
led_red = [0] * LED_COUNT
led_green = [0] * LED_COUNT
led_blue = [0] * LED_COUNT
videofiles = [n for n in os.listdir('../LEDS') if n.startswith('fx')]
cap = cv2.VideoCapture('../LEDS/fx1.mp4')
        
def set_leds(image):
    global led_red, led_green, led_blue
    image = cv2.resize(image, (int(math.sqrt(LED_COUNT)), int(math.sqrt(LED_COUNT))))
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            pixel = image[i, j]
            led_number = (i * 8) + j
            led_red[led_number] = pixel[2]
            led_green[led_number] = pixel[1]
            led_blue[led_number] = pixel[0]

def change_leds_video():
    global videofiles, cap
    target = random.choice(videofiles)
    cap = cv2.VideoCapture('../LEDS/' + target)
    cap.set(cv2.CAP_PROP_FPS, 10)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
def update_leds_video():
    global cap
    ret, frame = cap.read()
    if ret:
        set_leds(frame)
        time.sleep(0.02)
    else:
        change_leds_video()
    cv2.waitKey(1)