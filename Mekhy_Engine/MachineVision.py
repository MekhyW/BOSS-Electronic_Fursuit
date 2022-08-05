import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
target_point_x = 0 #mm
target_point_y = 0 #mm
target_point_z = 0 #mm
net = cv2.dnn.readNet("yolov5.weights", "yolov5.cfg")
avg_height_fursuit_head = 305
avg_height_human_head = 250
focal_length = 3.67
field_of_view = 78
distance_from_sensor_to_displays = 300

def unwrap_detection(input_image, output_data):
    class_ids = []
    confidences = []
    boxes = []
    rows = output_data.shape[0]
    image_width, image_height, _ = input_image.shape
    x_factor = image_width / 640
    y_factor =  image_height / 640
    for r in range(rows):
        row = output_data[r]
        confidence = row[4]
        if confidence >= 0.5:
            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]
            if (classes_scores[class_id] > .25):
                confidences.append(confidence)
                class_ids.append(class_id)
                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item() 
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)
    return class_ids, confidences, boxes

def getCameraFrame():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (800, 448))
    return frame

def depthFormula(object_size, label):
    if label == 0:
        depth = (focal_length * avg_height_fursuit_head) / object_size
    else:
        depth = (focal_length * avg_height_human_head) / object_size
    return depth

def xyFormula(depth, normalized_x, normalized_y, frame_width, frame_height):
    alpha = normalized_x * (field_of_view / frame_width)
    beta = normalized_y * (field_of_view / frame_height)
    x = depth * math.tan(math.radians(alpha))
    y = depth * math.tan(math.radians(beta)) - distance_from_sensor_to_displays
    return x, y

def calculateTargetPoint():
    global target_point_x
    global target_point_y
    global target_point_z
    frame = getCameraFrame()
    blob = cv2.dnn.blobFromImage(frame, 1/255, (640, 640), crop=False, swapRB=True)
    net.setInput(blob)
    predictions = net.forward()
    class_ids, confidences, boxes = unwrap_detection(frame, predictions)
    #take box with the largest area and use it to calculate the target point
    max_side = 0
    max_box = None
    label = 0
    for box_id in range(len(boxes)):
        side = max(boxes[box_id][2], boxes[box_id][3])
        if side > max_side:
            max_side = side
            max_box = boxes[box_id]
            label = class_ids[box_id]
    if max_box is not None:
        target_point_z = depthFormula(max_side, label)
        normalized_x = (max_box[0] + (max_box[2] / 2)) - (frame.shape[1] / 2)
        normalized_y = (max_box[1] + (max_box[3] / 2)) - (frame.shape[0] / 2)
        target_point_x, target_point_y = xyFormula(normalized_x, normalized_y, frame.shape[1], frame.shape[0])
        
