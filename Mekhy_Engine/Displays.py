import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import numpy as np
import cv2
import math
display_height = 480
display_width = 800
display_rotation = 30
left_eye_center = (340, 210)
right_eye_center = (1125, 210)
eye_neutral = cv2.imread('../Eyes/eye_neutral.png', cv2.COLOR_BGR2RGB)
mask = cv2.imread('../Eyes/mask.png', cv2.COLOR_BGR2RGB)

def composeEyes(expression, leftpos, rightpos):
    if expression == 0:
        eye = eye_neutral.copy()
    eyes = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    eyes[:] = (255, 255, 255)
    eyes[leftpos[1]:leftpos[1]+eye.shape[0], leftpos[0]:leftpos[0]+eye.shape[1]] = eye
    eyes[rightpos[1]:rightpos[1]+eye.shape[0], rightpos[0]:rightpos[0]+eye.shape[1]] = eye
    return eyes

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def rotateFrame(frame):
    firstHalf = frame[0:frame.shape[0], 0:int(frame.shape[1]/2)]
    secondHalf = frame[0:frame.shape[0], int(frame.shape[1]/2):frame.shape[1]]
    firstHalf = rotate_image(firstHalf, display_rotation)
    secondHalf = rotate_image(secondHalf, -display_rotation)
    y_nonzero, x_nonzero, _ = np.nonzero(firstHalf)
    firstHalf = firstHalf[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
    y_nonzero, x_nonzero, _ = np.nonzero(secondHalf)
    secondHalf = secondHalf[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
    firstHalf = cv2.resize(firstHalf, (display_width, display_height), interpolation = cv2.INTER_AREA)
    secondHalf = cv2.resize(secondHalf, (display_width, display_height), interpolation = cv2.INTER_AREA)
    frame = np.concatenate((firstHalf, secondHalf), axis = 1)
    return frame

def composeFrame(expression):
    frame = mask.copy()
    eyes = composeEyes(expression, left_eye_center, right_eye_center)
    frame[np.where((frame == [255, 255, 255]).all(axis = 2))] = eyes[np.where((frame == [255, 255, 255]).all(axis = 2))]
    frame = rotateFrame(frame)
    print(frame.shape)
    return frame

def GraphicsDraw(expression):
    cv2.imshow('Eyes', composeFrame(expression))
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        if "Eye" in window.get_name():
            window.maximize()
        elif "Terminal" in window.get_name():
            window.minimize()
    cv2.waitKey(1)