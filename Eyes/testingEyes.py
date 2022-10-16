import cv2
import numpy as np
import facemesh
display_height = 480
display_width = 800
display_rotation = 30
left_eye_center = (150, 107)
right_eye_center = (552, 107)
eye_radius_horizontal = 150
eye_radius_vertical = 180
eye = cv2.imread('eye_disgusted.png', cv2.COLOR_BGR2RGB)
eye_closed = cv2.imread('eye_closed.png', cv2.COLOR_BGR2RGB)
mask = cv2.VideoCapture('mask_disgusted.mp4')
import threading

def composeEyes(frame, leftpos, rightpos):
    eyes = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    eyes[:] = eye[0, 0]
    if facemesh.left_eye_closed:
        eyes[0:frame.shape[0], 0:int(frame.shape[1]/2)] = eye_closed[0:frame.shape[0], 0:int(frame.shape[1]/2)]
    else:
        eyes[leftpos[1]:leftpos[1]+eye.shape[0], leftpos[0]:leftpos[0]+eye.shape[1]] = eye
    if facemesh.right_eye_closed:
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

def composeFrame(mask):
    frame = mask.copy()
    lefteye_center_x = int(left_eye_center[0] + (eye_radius_horizontal*facemesh.displacement_eye[0]))
    lefteye_center_y = int(left_eye_center[1] + (eye_radius_vertical*facemesh.displacement_eye[1]))
    righteye_center_x = int(right_eye_center[0] + (eye_radius_horizontal*facemesh.displacement_eye[0]))
    righteye_center_y = int(right_eye_center[1] + (eye_radius_vertical*facemesh.displacement_eye[1]))
    eyes = composeEyes(frame, (lefteye_center_x, lefteye_center_y), (righteye_center_x, righteye_center_y))
    whiteregion = np.where((frame > 125).all(axis = 2))
    frame[whiteregion] = eyes[whiteregion]
    #frame = rotateFrame(frame)
    return frame

def machine_vision_thread_A():
    while True:
        try:
            facemesh.FacemeshRecognition()
            print(facemesh.left_eye_closed, facemesh.right_eye_closed)
        except Exception as e:
            print(e)

def machine_vision_thread_B():
    while True:
        try:
            facemesh.EmotionRecognition()
        except Exception as e:
            print(e)

def display_thread():
    while(mask.isOpened()):
        try:
            ret, frame = mask.read()
            if ret:
                frame = composeFrame(frame)
                cv2.imshow('frame', frame)
            else:
                mask.set(cv2.CAP_PROP_POS_FRAMES, 0)
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)

machine_vision_thread_A = threading.Thread(target=machine_vision_thread_A)
machine_vision_thread_B = threading.Thread(target=machine_vision_thread_B)
display_thread = threading.Thread(target=display_thread)
machine_vision_thread_A.start()
machine_vision_thread_B.start()
display_thread.start()