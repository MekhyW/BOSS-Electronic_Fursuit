import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import numpy as np
import cv2
import mediapipe as mp
import threading
frame = None
frame_facemesh = None
mesh_points = None
displacement_eye = (0,0)
left_eye_closed = False
right_eye_closed = False
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawSpec = mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
getFrameSemaphore = threading.Semaphore(0)
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (320,240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size = camera.resolution)
    using_csi = True
except Exception as e:
    print(e)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    using_csi = False

RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]
LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246] 
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
LEFT_EYEBROW = [383, 300, 293, 334, 296, 336, 285, 417]
RIGHT_EYEBROW = [156, 70, 63, 105, 66, 107, 55, 193]

def inference_facemesh(frame, drawing):
    global mesh_points
    frame_facemesh = frame.copy()
    H, W, _ = frame_facemesh.shape
    rgb_image = cv2.cvtColor(frame_facemesh, cv2.COLOR_BGR2RGB)
    results_mesh = face_mesh.process(rgb_image)
    if results_mesh.multi_face_landmarks:
        mesh_points=np.array([np.multiply([p.x, p.y], [W, H]).astype(int) for p in results_mesh.multi_face_landmarks[0].landmark])
        lex1, ley1 = np.min(mesh_points[LEFT_EYE], axis=0)
        lex2, ley2 = np.max(mesh_points[LEFT_EYE], axis=0)
        rex1, rey1 = np.min(mesh_points[RIGHT_EYE], axis=0)
        rex2, rey2 = np.max(mesh_points[RIGHT_EYE], axis=0)
        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
        displacement_left_eye = (2*(l_cx-((lex1+lex2)/2))/abs(lex2-lex1), 2*(l_cy-((ley1+ley2)/2))/abs((ley2-ley1)))
        displacement_right_eye = (2*(r_cx-((rex1+rex2)/2))/abs(rex2-rex1), 2*(r_cy-((rey1+rey2)/2))/abs((rey2-rey1)))
        displacement_eye = ((displacement_left_eye[0]+displacement_right_eye[0])/2, (displacement_left_eye[1]+displacement_right_eye[1])/2)
        if abs(lex1-lex2)/abs(ley1-ley2) > 5:
            left_eye_closed = True
        else:
            left_eye_closed = False
        if abs(rex1-rex2)/abs(rey1-rey2) > 5:
            right_eye_closed = True
        else:
            right_eye_closed = False
        if drawing:
            for faceLms in results_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame_facemesh, faceLms, mp_face_mesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
            cv2.rectangle(frame_facemesh, (lex1, ley1), (lex2, ley2), (0, 255, 0), 2)
            cv2.rectangle(frame_facemesh, (rex1, rey1), (rex2, rey2), (0, 255, 0), 2)
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv2.circle(frame_facemesh, tuple(center_left), int(l_radius), (255,0,255), 1, cv2.LINE_AA)
            cv2.circle(frame_facemesh, tuple(center_right), int(r_radius), (255,0,255), 1, cv2.LINE_AA)
        return frame_facemesh, displacement_eye, left_eye_closed, right_eye_closed
    return frame_facemesh, None, True, True

def FacemeshRecognition(drawing=False):
    global frame, frame_facemesh, displacement_eye, left_eye_closed, right_eye_closed
    if frame is None:
        return None
    frame_facemesh, de, left_eye_closed, right_eye_closed = inference_facemesh(frame, drawing)
    if de:
        displacement_eye = ((displacement_eye[0]*0.8)+(de[0]*0.2), (displacement_eye[1]*0.8)+(de[1]*0.2))
    displacement_eye = (max(min(1, displacement_eye[0]), -1), max(min(0.3, displacement_eye[1]), -0.3))    

def getFrameThread():
    global frame, using_csi
    while True:
        try:
            if using_csi:
                for captured in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                    rawCapture.truncate(0)
                    frame = captured.array
                    getFrameSemaphore.release()
            else:
                ret, frame = cap.read()
                getFrameSemaphore.release()
        except Exception as e:
            print(e)

def facemeshRecognitionThread(drawing=False):
    while True:
        try:
            getFrameSemaphore.acquire()
            FacemeshRecognition(drawing)
        except Exception as e:
            print(e)

def startThreads(drawing=False):
    global getFrameThread, facemeshRecognitionThread, emotionRecognitionThread
    getFrameThread = threading.Thread(target=getFrameThread)
    facemeshRecognitionThread = threading.Thread(target=facemeshRecognitionThread, args=(drawing,))
    getFrameThread.start()
    facemeshRecognitionThread.start()

if __name__ == '__main__':
    startThreads(drawing=True)
    while True:
        if left_eye_closed and right_eye_closed:
            print('BOTH EYES CLOSED')
        elif left_eye_closed:
            print('LEFT EYE CLOSED')
        elif right_eye_closed:
            print('RIGHT EYE CLOSED')
        else:
            print(displacement_eye)
        if frame_facemesh is not None:
            cv2.imshow('Facemesh', frame_facemesh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break