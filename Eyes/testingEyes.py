import cv2
import numpy as np
import facemesh
display_height = 480
display_width = 800
display_rotation = 30
left_eye_center = (150, 107)
right_eye_center = (552, 107)
eye_radius_horizontal = 120
eye_radius_vertical = 80
eye = cv2.imread('eye_neutral.png', cv2.COLOR_BGR2RGB)
mask = cv2.VideoCapture('mask_neutral.mp4')
import threading

def composeEyes(frame, leftpos, rightpos):
    eyes = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    eyes[:] = eye[0, 0]
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

def composeFrame(mask):
    frame = mask.copy()
    print(facemesh.displacement_eye)
    lefteye_center_x = int(left_eye_center[0] + (eye_radius_horizontal*facemesh.displacement_eye[0]))
    lefteye_center_y = int(left_eye_center[1] + (eye_radius_vertical*facemesh.displacement_eye[1]))
    righteye_center_x = int(right_eye_center[0] + (eye_radius_horizontal*facemesh.displacement_eye[0]))
    righteye_center_y = int(right_eye_center[1] + (eye_radius_vertical*facemesh.displacement_eye[1]))
    eyes = composeEyes(frame, (lefteye_center_x, lefteye_center_y), (righteye_center_x, righteye_center_y))
    whiteregion = np.where((frame > 125).all(axis = 2))
    frame[whiteregion] = eyes[whiteregion]
    #frame = rotateFrame(frame)
    return frame

def machine_vision_thread():
    while True:
        facemesh.FacialRecognition()

def display_thread():
    while(mask.isOpened()):
        ret, frame = mask.read()
        if ret:
            frame = composeFrame(frame)
            cv2.imshow('frame', frame)
        else:
            mask.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cv2.waitKey(1)

machine_vision_thread = threading.Thread(target=machine_vision_thread)
display_thread = threading.Thread(target=display_thread)
machine_vision_thread.start()
display_thread.start()