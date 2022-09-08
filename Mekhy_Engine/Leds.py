import cv2
import numpy as np
led_red = [0] * 64
led_green = [0] * 64
led_blue = [0] * 64

def set_leds(image):
    global led_red, led_green, led_blue
    image = cv2.resize(image, (8, 8))
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            pixel = image[i, j]
            led_number = (i * 8) + j
            led_red[led_number] = pixel[2]
            led_green[led_number] = pixel[1]
            led_blue[led_number] = pixel[0]