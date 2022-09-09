import cv2
import numpy as np
import math
LED_COUNT = 256
led_red = [0] * LED_COUNT
led_green = [0] * LED_COUNT
led_blue = [0] * LED_COUNT

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