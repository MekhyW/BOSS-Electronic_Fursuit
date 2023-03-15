import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import MachineVision
import numpy as np
import cv2
import os
import random
import time
display_height = 480
display_width = 800
display_rotation = 30
distance_between_displays = 150
left_eye_center = (150, 97)
right_eye_center = (552, 97)
eye_radius_horizontal = 150
eye_radius_vertical = 180
eye_closed = cv2.imread('../Eyes/eye_closed.png', cv2.COLOR_BGR2RGB)
eye_neutral = cv2.imread('../Eyes/eye_neutral.png', cv2.COLOR_BGR2RGB)
eye_sad = cv2.imread('../Eyes/eye_sad.png', cv2.COLOR_BGR2RGB)
eye_happy = cv2.imread('../Eyes/eye_happy.png', cv2.COLOR_BGR2RGB)
eye_scared = cv2.imread('../Eyes/eye_scared.png', cv2.COLOR_BGR2RGB)
eye_angry = cv2.imread('../Eyes/eye_angry.png', cv2.COLOR_BGR2RGB)
eye_disgusted = cv2.imread('../Eyes/eye_disgusted.png', cv2.COLOR_BGR2RGB)
eye_heart = cv2.imread('../Eyes/eye_heart.png', cv2.COLOR_BGR2RGB)
eye_hypnotic = cv2.imread('../Eyes/eye_hipnotic.png', cv2.COLOR_BGR2RGB)
eye_sexy = cv2.imread('../Eyes/eye_sexy.png', cv2.COLOR_BGR2RGB)
eye_demonic = cv2.imread('../Eyes/eye_demonic.png', cv2.COLOR_BGR2RGB)
mask_neutral = cv2.VideoCapture('../Eyes/mask_neutral.mp4')
mask_sad = cv2.VideoCapture('../Eyes/mask_sad.mp4')
mask_happy = cv2.VideoCapture('../Eyes/mask_happy.mp4')
mask_scared = cv2.VideoCapture('../Eyes/mask_scared.mp4')
mask_angry = cv2.VideoCapture('../Eyes/mask_angry.mp4')
mask_disgusted = cv2.VideoCapture('../Eyes/mask_disgusted.mp4')
mask_heart = cv2.VideoCapture('../Eyes/mask_heart.mp4')
mask_hypnotic = cv2.VideoCapture('../Eyes/mask_hipnotic.mp4')
mask_sexy = cv2.VideoCapture('../Eyes/mask_sexy.mp4')
mask_demonic = cv2.VideoCapture('../Eyes/mask_demonic.mp4')
cached_expression = 0
cached_expression_time = 0
playingvideo = False

def composeEyes(frame, eye, leftpos, rightpos):
    eyes = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    eyes[:] = eye[0, 0]
    if MachineVision.left_eye_closed:
        eyes[0:frame.shape[0], 0:int(frame.shape[1]/2)] = eye_closed[0:frame.shape[0], 0:int(frame.shape[1]/2)]
    else:
        eyes[leftpos[1]:leftpos[1]+eye.shape[0], leftpos[0]:leftpos[0]+eye.shape[1]] = eye
    if MachineVision.right_eye_closed:
        eyes[0:frame.shape[0], int(frame.shape[1]/2):frame.shape[1]] = eye_closed[0:frame.shape[0], int(frame.shape[1]/2):frame.shape[1]]
    else:
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

def composeFrame(eye, frame, displacement_eye):
    lefteye_center_x = int(left_eye_center[0] + (eye_radius_horizontal*displacement_eye[0]))
    lefteye_center_y = int(left_eye_center[1] + (eye_radius_vertical*displacement_eye[1]))
    righteye_center_x = int(right_eye_center[0] + (eye_radius_horizontal*displacement_eye[0]))
    righteye_center_y = int(right_eye_center[1] + (eye_radius_vertical*displacement_eye[1]))
    eyes = composeEyes(frame, eye, (lefteye_center_x, lefteye_center_y), (righteye_center_x, righteye_center_y))
    whiteregion = np.where((frame > 80).all(axis = 2))
    frame[whiteregion] = eyes[whiteregion]
    frame = rotateFrame(frame)
    return frame

def ManageWindows():
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        window_name = window.get_name()
        if "Eyes" in window_name:
            window.maximize()
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.X, 0, 0, display_width, display_height)
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.Y, 0, 0, display_width, display_height)
        elif "Terminal" in window_name:
            window.minimize()

def PlayVideo(file_name, remove_file=True):
    global playingvideo
    playingvideo = True
    cap = cv2.VideoCapture(file_name)
    while(cap.isOpened() and playingvideo):
        ret, frame = cap.read()
        if ret:
            #resized = cv2.resize(frame, (display_width, display_height), interpolation = cv2.INTER_AREA)
            #duplicated = cv2.hconcat([resized, resized])
            #cv2.imshow('Eyes', duplicated)
            cv2.imshow('Eyes', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
        ManageWindows()
    cap.release()
    playingvideo = False
    if remove_file:
        os.remove(file_name)

def GraphicsRefresh(expression, displacement_eye):
    global cached_expression, cached_expression_time
    if expression != cached_expression:
        if time.time() - cached_expression_time > 1:
            cached_expression = expression
    else:
        cached_expression_time = time.time()
    if cached_expression == 0:
        eye = eye_neutral
        mask = mask_neutral
    elif cached_expression == 1:
        eye = eye_angry
        mask = mask_angry
    elif cached_expression == 2:
        eye = eye_disgusted
        mask = mask_disgusted
    elif cached_expression == 3:
        eye = eye_sad
        mask = mask_sad
    elif cached_expression == 4:
        eye = eye_happy
        mask = mask_happy
    elif cached_expression == 5:
        eye = eye_scared
        mask = mask_scared
    elif cached_expression == 6:
        eye = eye_heart
        mask = mask_heart
    elif cached_expression == 7:
        eye = eye_hypnotic
        mask = mask_hypnotic
    elif cached_expression == 8:
        eye = eye_sexy
        mask = mask_sexy
    elif cached_expression == 9:
        eye = eye_demonic
        mask = mask_demonic
    if not playingvideo:
        ret, frame = mask.read()
        if ret:
            frame = composeFrame(eye, frame, displacement_eye)
            cv2.imshow('Eyes', frame)
        else:
            mask.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ManageWindows()

if __name__ == '__main__':
    PlayVideo('resources/small.mp4', False)
    for exp in range(10):
        x = random.uniform(-1, 1)
        y = random.uniform(-0.3, 0.3)
        for n in range(50):
            GraphicsRefresh(exp, (x, y))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break