import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import MachineVision
import numpy as np
import cv2
import os
import random
import time
import threading
display_height = 480
display_width = 800
display_rotation = 30
left_eye_center = (150, 97)
right_eye_center = (552, 97)
displacement_eye = (0, 0)
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
rot_mat_positive = cv2.getRotationMatrix2D((225,197), 30, 1.0)
rot_mat_negative = cv2.getRotationMatrix2D((225,197), -30, 1.0)
eye = eye_neutral
mask = mask_neutral
eyes = np.full((display_height, display_width, 3), eye_neutral[0, 0], dtype=np.uint8)
frame_template = np.full((display_height, display_width, 3), eye_neutral[0, 0], dtype=np.uint8)
frame_with_eyes = np.full((display_height, display_width, 3), eye_neutral[0, 0], dtype=np.uint8)
frame_rotated = np.full((display_height, display_width, 3), eye_neutral[0, 0], dtype=np.uint8)
composeEyesSemaphore = threading.Semaphore(0)
applyEyesSemaphore = threading.Semaphore(0)

def rotate_image(image, angle):
    #image_center = tuple(np.array(image.shape[1::-1]) / 2)
    if angle == display_rotation:
        rot_mat = rot_mat_positive
    elif angle == -display_rotation:
        rot_mat = rot_mat_negative
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def composeEyes():
    global frame_template, eyes
    lefteye_center_x = int(left_eye_center[0] + (eye_radius_horizontal*displacement_eye[0]))
    lefteye_center_y = int(left_eye_center[1] + (eye_radius_vertical*displacement_eye[1]))
    righteye_center_x = int(right_eye_center[0] + (eye_radius_horizontal*displacement_eye[0]))
    righteye_center_y = int(right_eye_center[1] + (eye_radius_vertical*displacement_eye[1]))
    leftpos = (lefteye_center_x, lefteye_center_y)
    rightpos = (righteye_center_x, righteye_center_y)
    eyes_local = np.full((frame_template.shape[0], frame_template.shape[1], 3), eye[0, 0], dtype=np.uint8)
    if MachineVision.left_eye_closed:
        eyes_local[0:frame_template.shape[0], 0:int(frame_template.shape[1]/2)] = eye_closed[0:frame_template.shape[0], 0:int(frame_template.shape[1]/2)]
    else:
        eyes_local[leftpos[1]:leftpos[1] + eye.shape[0], leftpos[0]:leftpos[0] + eye.shape[1]] = eye
    if MachineVision.right_eye_closed:
        eyes_local[0:frame_template.shape[0], int(frame_template.shape[1]/2):frame_template.shape[1]] = eye_closed[0:frame_template.shape[0], int(frame_template.shape[1]/2):frame_template.shape[1]]
    else:
        eyes_local[rightpos[1]:rightpos[1] + eye.shape[0], rightpos[0]:rightpos[0] + eye.shape[1]] = eye
    eyes = eyes_local

def applyEyes():
    global frame_template, eyes, frame_with_eyes
    whiteregion = np.where((frame_template > 80).all(axis = 2))
    frame_with_eyes_local = frame_template.copy()
    frame_with_eyes_local[whiteregion] = eyes[whiteregion]
    frame_with_eyes = frame_with_eyes_local

def rotateFrame():
    global frame_with_eyes, frame_rotated
    firstHalf = frame_with_eyes[0:frame_with_eyes.shape[0], 0:int(frame_with_eyes.shape[1]/2)]
    secondHalf = frame_with_eyes[0:frame_with_eyes.shape[0], int(frame_with_eyes.shape[1]/2):frame_with_eyes.shape[1]]
    firstHalf = rotate_image(firstHalf, display_rotation)
    secondHalf = rotate_image(secondHalf, -display_rotation)
    y_nonzero, x_nonzero, _ = np.nonzero(firstHalf)
    firstHalf = firstHalf[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
    y_nonzero, x_nonzero, _ = np.nonzero(secondHalf)
    secondHalf = secondHalf[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
    firstHalf = cv2.resize(firstHalf, (display_width, display_height), interpolation = cv2.INTER_NEAREST)
    secondHalf = cv2.resize(secondHalf, (display_width, display_height), interpolation = cv2.INTER_NEAREST)
    frame_rotated = np.concatenate((firstHalf, secondHalf), axis = 1)

def ManageWindows():
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        window_name = window.get_name()
        window_name = window_name.lower()
        if "eyes" in window_name:
            window.maximize()
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.X, 0, 0, display_width, display_height)
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.Y, 0, 0, display_width, display_height)
            window.set_window_type_hint(Wnck.WindowTypeHint.DOCK)
        elif any([x in window_name for x in ["terminal", "sh", "play"]]):
            window.minimize()

def PlayVideo(file_name, remove_file=True):
    global playingvideo
    ManageWindows()
    playingvideo = True
    cap = cv2.VideoCapture(file_name)
    while(cap.isOpened() and playingvideo):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Eyes', frame)
            cv2.waitKey(1)
        else:
            break
    cap.release()
    playingvideo = False
    if remove_file:
        os.remove(file_name)
    ManageWindows()

def GraphicsRefresh(expression):
    global cached_expression, cached_expression_time, frame_template, frame_rotated, eye, mask
    if expression != cached_expression:
        if time.time() - cached_expression_time > 1:
            cached_expression = expression
            ManageWindows()
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
        ret, frame_template = mask.read()
        if ret:
            cv2.imshow('Eyes', frame_rotated)
        else:
            mask.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ManageWindows()

def composeEyesThread():
    while True:
        try:
            if not playingvideo:
                composeEyes()
                composeEyesSemaphore.release()
        except Exception as e:
            print(e)

def applyEyesThread():
    while True:
        try:
            composeEyesSemaphore.acquire()
            applyEyes()
            applyEyesSemaphore.release()
        except Exception as e:
            print(e)

def rotateFrameThread():
    while True:
        try:
            applyEyesSemaphore.acquire()
            rotateFrame()
        except Exception as e:
            print(e)

def startThreads():
    global composeEyesThread, applyEyesThread, rotateFrameThread
    cv2.imshow('Eyes', frame_rotated)
    composeEyesThread = threading.Thread(target=composeEyesThread)
    applyEyesThread = threading.Thread(target=applyEyesThread)
    rotateFrameThread = threading.Thread(target=rotateFrameThread)
    composeEyesThread.priority = 3
    applyEyesThread.priority = 3
    rotateFrameThread.priority = 3
    composeEyesThread.start()
    applyEyesThread.start()
    rotateFrameThread.start()

if __name__ == '__main__':
    startThreads()
    PlayVideo('resources/small.mp4', False)
    for exp in range(10):
        x = random.uniform(-1, 1)
        y = random.uniform(-0.3, 0.3)
        displacement_eye = (x, y)
        for n in range(200):
            GraphicsRefresh(exp)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
    quit()