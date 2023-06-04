import numpy as np
import cv2
import mediapipe as mp
import pickle
import threading
displacement_eye = (0,0)
left_eye_closed = False
right_eye_closed = False
AutomaticExpression = 'Neutral'
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawSpec = mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mesh_points = None
emotion_model = pickle.load(open('resources/emotion_model.pkl', 'rb'))
facemeshRecognitionSemaphore = threading.Semaphore(0)
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (320,240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size = camera.resolution)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    using_csi = True
except Exception as e:
    print(e)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    cap.set(cv2.CAP_PROP_AUTO_WB, 1)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    using_csi = False

RIGHT_EYE =[362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]
LEFT_EYE=[33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246] 
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
LEFT_EYEBROW = [383, 300, 293, 334, 296, 336, 285, 417]
RIGHT_EYEBROW = [156, 70, 63, 105, 66, 107, 55, 193]

def inference_facemesh(image, drawing):
    global mesh_points
    frame = image.copy()
    H, W, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
        if abs(lex1-lex2)/abs(ley1-ley2) > 4:
            left_eye_closed = True
        else:
            left_eye_closed = False
        if abs(rex1-rex2)/abs(rey1-rey2) > 4:
            right_eye_closed = True
        else:
            right_eye_closed = False
        if drawing:
            for faceLms in results_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, faceLms, mp_face_mesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
            cv2.rectangle(frame, (lex1, ley1), (lex2, ley2), (0, 255, 0), 2)
            cv2.rectangle(frame, (rex1, rey1), (rex2, rey2), (0, 255, 0), 2)
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv2.circle(frame, center_left, int(l_radius), (255,0,255), 1, cv2.LINE_AA)
            cv2.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv2.LINE_AA)
        return frame, displacement_eye, left_eye_closed, right_eye_closed
    return frame, None, True, True

def getFrame():
    if using_csi:
        rawCapture.truncate(0)
        camera.capture(rawCapture, resize=camera.resolution, format="bgr")
        frame = rawCapture.array
    else:
        ret, frame = cap.read()
    return frame

def FacemeshRecognition(drawing=False):
    global displacement_eye, left_eye_closed, right_eye_closed
    frame = getFrame()
    frame, de, left_eye_closed, right_eye_closed = inference_facemesh(frame, drawing)
    if de:
        displacement_eye = ((displacement_eye[0]*0.8)+(de[0]*0.2), (displacement_eye[1]*0.8)+(de[1]*0.2))
    displacement_eye = (max(min(1, displacement_eye[0]), -1), max(min(0.3, displacement_eye[1]), -0.3))
    return frame    

def predict_emotion():
    global mesh_points, emotion_model, AutomaticExpression
    if mesh_points is None:
        return None
    nose_tip = mesh_points[4]
    chin_tip = mesh_points[152]
    mesh_norm = mesh_points - nose_tip
    scale_factor = np.linalg.norm(chin_tip - nose_tip)
    mesh_norm = np.divide(mesh_norm, scale_factor)
    landmarks_flat = mesh_norm.flatten()
    pred = emotion_model.predict([landmarks_flat])
    AutomaticExpression = pred[0].capitalize()

if __name__ == '__main__':
    while True:
        frame = FacemeshRecognition(drawing=True)
        predict_emotion()
        print(AutomaticExpression)
        if left_eye_closed and right_eye_closed:
            print('BOTH EYES CLOSED')
        elif left_eye_closed:
            print('LEFT EYE CLOSED')
        elif right_eye_closed:
            print('RIGHT EYE CLOSED')
        else:
            print(displacement_eye)
        cv2.imshow('Facemesh', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break