


from ultralytics import YOLO
import cv2
import numpy as np
import os
import time
from datetime import datetime

RUN_DETECTION = True
LAST_ALERT_TIME = 0

foreign_object_model_path = r"C:\Users\kaswa\OneDrive\Desktop\mca project\detectionproject\myapp\core\runs\train\railway_foreign_object_detection\weights\best.pt"
track_model_path = r"C:\Users\kaswa\OneDrive\Desktop\mca project\detectionproject\myapp\core\track_new\best.pt"

object_model = YOLO(foreign_object_model_path)
track_model = YOLO(track_model_path)


def compute_iou(box1, box2):

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter = max(0, x2-x1) * max(0, y2-y1)

    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])

    return inter / (area1 + area2 - inter + 1e-6)


def box_distance(boxA, boxB):

    ax1, ay1, ax2, ay2 = boxA
    bx1, by1, bx2, by2 = boxB

    dx = max(bx1 - ax2, ax1 - bx2, 0)
    dy = max(by1 - ay2, ay1 - by2, 0)

    return np.sqrt(dx*dx + dy*dy)


def process_frame(frame, camera):

    global LAST_ALERT_TIME

    frame = cv2.resize(frame,(480,640))

    results_objects = object_model(frame,conf=0.35,verbose=False)
    results_track = track_model(frame,conf=0.1,verbose=False)

    object_boxes=[]
    object_classes=[]
    object_names=[]

    if results_objects and results_objects[0].boxes is not None:

        object_boxes = results_objects[0].boxes.xyxy.cpu().numpy()
        object_classes = results_objects[0].boxes.cls.cpu().numpy()
        object_names = results_objects[0].names


    track_boxes=[]
    track_classes=[]
    track_names=[]

    if results_track and results_track[0].boxes is not None:

        track_boxes = results_track[0].boxes.xyxy.cpu().numpy()
        track_classes = results_track[0].boxes.cls.cpu().numpy()
        track_names = results_track[0].names


    rail_track_boxes=[]

    for i,box in enumerate(track_boxes):

        if track_names[int(track_classes[i])] == "rail-track":

            rail_track_boxes.append(box)


    combined_frame = frame.copy()


    for box in rail_track_boxes:

        x1,y1,x2,y2 = map(int,box)

        cv2.rectangle(combined_frame,(x1,y1),(x2,y2),(0,255,255),3)

        cv2.putText(
            combined_frame,
            "rail-track",
            (x1,y1-8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )


    for i,obj_box in enumerate(object_boxes):

        x1,y1,x2,y2 = map(int,obj_box)

        obj_class = object_names[int(object_classes[i])]

        high_risk=False

        for track_box in rail_track_boxes:

            iou = compute_iou(obj_box,track_box)

            pixel_dist = box_distance(obj_box,track_box)

            track_width_px = abs(track_box[2] - track_box[0])

            meter_per_pixel = 1.435 / max(track_width_px,1)

            distance_m = pixel_dist * meter_per_pixel

            if iou > 0.1 or distance_m <= 1.0:

                high_risk=True
                break


        cv2.rectangle(combined_frame,(x1,y1),(x2,y2),(255,255,0),2)

        if high_risk:

            label=f"{obj_class} | HIGH RISK"
            color=(0,0,255)

            current_time = time.time()

            if current_time - LAST_ALERT_TIME >= 5:

                LAST_ALERT_TIME = current_time

                filename = datetime.now().strftime("%Y%m%d%H%M%S%f")+".jpg"

                save_path = os.path.join("media/alert",filename)

                os.makedirs("media/alert", exist_ok=True)

                cv2.imwrite(save_path,combined_frame)

                try:

                    from myapp.models import Cameraalert, Locopilot

                    pilot = None

                    if camera and camera.TRAIN:
                        pilot = Locopilot.objects.filter(TRAIN=camera.TRAIN).first()

                    Cameraalert.objects.create(
                        CAMERA=camera,
                        LOCOPILOT=pilot,
                        Image="alert/"+filename,
                        description=obj_class+" detected on track",
                        date=str(datetime.now().date())
                    )

                    print("ALERT SAVED:", obj_class)

                except Exception as e:

                    print("DB ERROR:", e)

        else:

            label=f"{obj_class} | LOW RISK"
            color=(0,255,0)


        cv2.putText(
            combined_frame,
            label,
            (x1,max(y1-10,20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return combined_frame


def run_detection_stream(video_source, camera=None, locopilot=None):

    global RUN_DETECTION

    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        return

    frame_skip = 2
    frame_count = 0

    while RUN_DETECTION:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % frame_skip != 0:
            continue

        combined_frame = process_frame(frame, camera)

        ret, buffer = cv2.imencode('.jpg', combined_frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()