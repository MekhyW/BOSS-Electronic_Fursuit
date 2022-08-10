import cv2
import numpy as np
display_height = 480
display_width = 800
display_rotation = 30
left_eye_center = (340, 210)
right_eye_center = (1125, 210)
eye = cv2.imread('eye.png', cv2.COLOR_BGR2RGB)
mask = cv2.imread('mask.png', cv2.COLOR_BGR2RGB)

def composeEyes(leftpos, rightpos):
    eyes = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
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

def composeFrame():
    frame = mask.copy()
    eyes = composeEyes(left_eye_center, right_eye_center)
    frame[np.where((frame == [255, 255, 255]).all(axis = 2))] = eyes[np.where((frame == [255, 255, 255]).all(axis = 2))]
    #frame = rotateFrame(frame)
    print(frame.shape)
    return frame

while True:
    cv2.imshow('frame', composeFrame())
    cv2.waitKey(1)
