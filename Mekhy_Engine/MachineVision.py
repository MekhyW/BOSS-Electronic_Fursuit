import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
from keras.models import Sequential
from keras.layers import Rescaling
from keras.layers import Conv2D, MaxPool2D, Dense, Dropout, Flatten
from keras.layers import BatchNormalization
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
displacement_eye = (0,0)
left_eye_closed = False
right_eye_closed = False
AutomaticExpression = 'Neutral'
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawSpec = mp_drawing.DrawingSpec(thickness=1, circle_radius=2)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
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

emotions = {
    0: ['Angry', (0,0,255), (255,255,255)],
    1: ['Disgusted', (0,102,0), (255,255,255)],
    2: ['Scared', (255,255,153), (0,51,51)],
    3: ['Happy', (153,0,153), (255,255,255)],
    4: ['Sad', (255,0,0), (255,255,255)],
    5: ['Scared', (0,255,0), (255,255,255)],
    6: ['Neutral', (160,160,160), (255,255,255)]
}
num_classes = len(emotions)
input_shape = (48, 48, 1)
weights_1 = 'resources/vggnet.h5'
weights_2 = 'resources/vggnet_up.h5'

class VGGNet(Sequential):
    def __init__(self, input_shape, num_classes, checkpoint_path, lr=1e-3):
        super().__init__()
        self.add(Rescaling(1./255, input_shape=input_shape))
        self.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal'))
        self.add(BatchNormalization())
        self.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.5))
        self.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.4))
        self.add(Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.5))
        self.add(Conv2D(512, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(512, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.4))
        self.add(Flatten())
        self.add(Dense(1024, activation='relu'))
        self.add(Dropout(0.5))
        self.add(Dense(256, activation='relu'))
        self.add(Dense(num_classes, activation='softmax'))
        self.compile(optimizer=Adam(learning_rate=lr),
                    loss=categorical_crossentropy,
                    metrics=['accuracy'])
        self.checkpoint_path = checkpoint_path

def resize_face(face):
    x = tf.expand_dims(tf.convert_to_tensor(face), axis=2)
    return tf.image.resize(x, (48,48))

def recognition_preprocessing(faces):
    x = tf.convert_to_tensor([resize_face(f) for f in faces])
    return x

def inference_emotionrecog(image):
    frame = image.copy()
    H, W, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_image)
    if results.detections:
        faces = []
        pos = []
        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * W)
            y = int(box.ymin * H)
            w = int(box.width * W)
            h = int(box.height * H)
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(x + w, W)
            y2 = min(y + h, H)
            face = image[y1:y2,x1:x2]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            faces.append(face)
            pos.append((x1, y1, x2, y2))
        x = recognition_preprocessing(faces)
        y_2 = model_2.predict(x, verbose=0)
        l = np.argmax(y_2, axis=1)
        for i in range(len(faces)):
            cv2.rectangle(frame, (pos[i][0],pos[i][1]),
                            (pos[i][2],pos[i][3]), emotions[l[i]][1], 2, lineType=cv2.LINE_AA)
            cv2.rectangle(frame, (pos[i][0],pos[i][1]-20),
                            (pos[i][2]+20,pos[i][1]), emotions[l[i]][1], -1, lineType=cv2.LINE_AA)
            cv2.putText(frame, f'{emotions[l[i]][0]}', (pos[i][0],pos[i][1]-5),
                            0, 0.6, emotions[l[i]][2], 2, lineType=cv2.LINE_AA)
        return frame, emotions[l[i]][0]
    return frame, AutomaticExpression

def inference_facemesh(image):
    frame = image.copy()
    H, W, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_image)
    results_mesh = face_mesh.process(rgb_image)
    if results.detections:
        faces = []
        pos = []
        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * W)
            y = int(box.ymin * H)
            w = int(box.width * W)
            h = int(box.height * H)
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(x + w, W)
            y2 = min(y + h, H)
            face = image[y1:y2,x1:x2]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            faces.append(face)
            pos.append((x1, y1, x2, y2))
    if results_mesh.multi_face_landmarks:
        for faceLms in results_mesh.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, faceLms, mp_face_mesh.FACEMESH_CONTOURS,drawSpec,drawSpec)
        mesh_points=np.array([np.multiply([p.x, p.y], [W, H]).astype(int) for p in results_mesh.multi_face_landmarks[0].landmark])
        lex1, ley1 = np.min(mesh_points[LEFT_EYE], axis=0)
        lex2, ley2 = np.max(mesh_points[LEFT_EYE], axis=0)
        cv2.rectangle(frame, (lex1, ley1), (lex2, ley2), (0, 255, 0), 2)
        rex1, rey1 = np.min(mesh_points[RIGHT_EYE], axis=0)
        rex2, rey2 = np.max(mesh_points[RIGHT_EYE], axis=0)
        cv2.rectangle(frame, (rex1, rey1), (rex2, rey2), (0, 255, 0), 2)
        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
        center_left = np.array([l_cx, l_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)
        cv2.circle(frame, center_left, int(l_radius), (255,0,255), 1, cv2.LINE_AA)
        cv2.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv2.LINE_AA)
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
        return frame, displacement_eye, left_eye_closed, right_eye_closed
    return frame, None, True, True

model_1 = VGGNet(input_shape, num_classes, weights_1)
model_2 = VGGNet(input_shape, num_classes, weights_2)
model_1.load_weights(model_1.checkpoint_path)
model_2.load_weights(model_2.checkpoint_path)

def getFrame():
    if using_csi:
        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array
    else:
        ret, frame = cap.read()
    return frame

def FacemeshRecognition():
    global displacement_eye, left_eye_closed, right_eye_closed
    frame = getFrame()
    frame, de, left_eye_closed, right_eye_closed = inference_facemesh(frame)
    if de:
        displacement_eye = ((displacement_eye[0]*0.8)+(de[0]*0.2), (displacement_eye[1]*0.8)+(de[1]*0.2))
    displacement_eye = (max(min(1, displacement_eye[0]), -1), max(min(0.3, displacement_eye[1]), -0.3))
    return frame    

def EmotionRecognition():
    global AutomaticExpression
    frame = getFrame()
    frame, AutomaticExpression = inference_emotionrecog(frame)
    return frame

if __name__ == '__main__':
    while True:
        frameA = FacemeshRecognition()
        frameB = EmotionRecognition()
        frame = cv2.hconcat([frameA, frameB])
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