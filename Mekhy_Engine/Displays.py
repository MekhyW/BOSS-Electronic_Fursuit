import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import numpy as np
import cv2
import math, os
display_height = 480
display_width = 800
display_rotation = 30
distance_between_displays = 150
left_eye_center = (340, 210)
right_eye_center = (1125, 210)
leftpos = left_eye_center
rightpos = right_eye_center
eye_neutral = cv2.imread('../Eyes/eye_neutral.png', cv2.COLOR_BGR2RGB)
eye_sad = cv2.imread('../Eyes/eye_sad.png', cv2.COLOR_BGR2RGB)
eye_happy = cv2.imread('../Eyes/eye_happy.png', cv2.COLOR_BGR2RGB)
mask_neutral = cv2.imread('../Eyes/mask.png', cv2.COLOR_BGR2RGB)
mask_sad = cv2.imread('../Eyes/mask_sad.png', cv2.COLOR_BGR2RGB)
mask_happy = cv2.imread('../Eyes/mask_happy.png', cv2.COLOR_BGR2RGB)
playingvideo = False

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def composeEyes(eye, mask, target_position):
    eyes = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    eyes[:] = eye[0, 0]
    target_point_x, target_point_y, target_point_z = target_position
    leftpos_x = map(math.atan2(target_point_z, target_point_x+(distance_between_displays/2)), 0, 2*math.pi, left_eye_center[0]+left_eye_center[1], left_eye_center[0]-left_eye_center[1])
    leftpos_y = map(math.atan2(target_point_z, target_point_y), 0, 2*math.pi, 0, 2*left_eye_center[1])
    rightpos_x = map(math.atan2(target_point_z, target_point_x-(distance_between_displays/2)), 0, 2*math.pi, right_eye_center[0]-right_eye_center[1], right_eye_center[0]+right_eye_center[1])
    rightpos_y = map(math.atan2(target_point_z, target_point_y), 0, 2*math.pi, 0, 2*right_eye_center[1])
    leftpos = (int(leftpos_x), int(leftpos_y))
    rightpos = (int(rightpos_x), int(rightpos_y))
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

def composeFrame(expression, target_position):
    if expression == 0:
        eye = eye_neutral.copy()
        mask = mask_neutral.copy()
    elif expression == 3:
        eye = eye_sad.copy()
        mask = mask_sad.copy()
    elif expression == 4:
        eye = eye_happy.copy()
        mask = mask_happy.copy()
    frame = mask
    eyes = composeEyes(eye, mask, target_position)
    frame[np.where((frame == [255, 255, 255]).all(axis = 2))] = eyes[np.where((frame == [255, 255, 255]).all(axis = 2))]
    frame = rotateFrame(frame)
    print(frame.shape)
    return frame

def PlayVideo(file_name):
    global playingvideo
    playingvideo = True
    cap = cv2.VideoCapture(file_name)
    while(cap.isOpened() and playingvideo):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Eyes', frame)
        else:
            break
    cap.release()
    os.remove(file_name)
    playingvideo = False

def GraphicsRefresh(expression, target_position):
    if not playingvideo:
        cv2.imshow('Eyes', composeFrame(expression, target_position))
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        if "Eyes" in window.get_name():
            window.maximize()
        elif "Terminal" in window.get_name():
            window.minimize()
    cv2.waitKey(1)