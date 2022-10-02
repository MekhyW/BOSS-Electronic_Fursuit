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
eye_scared = cv2.imread('../Eyes/eye_scared.png', cv2.COLOR_BGR2RGB)
eye_angry = cv2.imread('../Eyes/eye_angry.png', cv2.COLOR_BGR2RGB)
eye_disgusted = cv2.imread('../Eyes/eye_disgusted.png', cv2.COLOR_BGR2RGB)
eye_heart = cv2.imread('../Eyes/eye_heart.png', cv2.COLOR_BGR2RGB)
eye_hypnotic = cv2.imread('../Eyes/eye_hypnotic.png', cv2.COLOR_BGR2RGB)
eye_sexy = cv2.imread('../Eyes/eye_sexy.png', cv2.COLOR_BGR2RGB)
eye_demonic = cv2.imread('../Eyes/eye_demonic.png', cv2.COLOR_BGR2RGB)
mask_neutral = cv2.VideoCapture('../Eyes/mask_neutral.mp4')
mask_sad = cv2.VideoCapture('../Eyes/mask_sad.mp4')
mask_happy = cv2.VideoCapture('../Eyes/mask_happy.mp4')
mask_scared = cv2.VideoCapture('../Eyes/mask_scared.mp4')
mask_angry = cv2.VideoCapture('../Eyes/mask_angry.mp4')
mask_disgusted = cv2.VideoCapture('../Eyes/mask_disgusted.mp4')
mask_heart = cv2.VideoCapture('../Eyes/mask_heart.mp4')
mask_hypnotic = cv2.VideoCapture('../Eyes/mask_hypnotic.mp4')
mask_sexy = cv2.VideoCapture('../Eyes/mask_sexy.mp4')
mask_demonic = cv2.VideoCapture('../Eyes/mask_demonic.mp4')
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

def composeFrame(eye, mask, target_position):
    frame = mask.copy()
    eyes = composeEyes(eye, mask, target_position)
    whiteregion = np.where((frame > 240).all(axis = 2))
    frame[whiteregion] = eyes[whiteregion]
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
    if expression == 0:
        eye = eye_neutral
        mask = mask_neutral
    elif expression == 1:
        eye = eye_angry
        mask = mask_angry
    elif expression == 2:
        eye = eye_disgusted
        mask = mask_disgusted
    elif expression == 3:
        eye = eye_sad
        mask = mask_sad
    elif expression == 4:
        eye = eye_happy
        mask = mask_happy
    elif expression == 5:
        eye = eye_scared
        mask = mask_scared
    elif expression == 6:
        eye = eye_heart
        mask = mask_heart
    elif expression == 7:
        eye = eye_hypnotic
        mask = mask_hypnotic
    elif expression == 8:
        eye = eye_sexy
        mask = mask_sexy
    elif expression == 9:
        eye = eye_demonic
        mask = mask_demonic
    if not playingvideo:
        ret, frame = mask.read()
        if ret:
            frame = composeFrame(eye, frame, target_position)
            cv2.imshow('frame', frame)
        else:
            mask.set(cv2.CAP_PROP_POS_FRAMES, 0)
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        if "Eyes" in window.get_name():
            window.maximize()
        elif "Terminal" in window.get_name():
            window.minimize()
    cv2.waitKey(1)