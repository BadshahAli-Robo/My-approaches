#this code is still under progress, I took some help from the google and youtube.


import cv2
import numpy as np
from object_detection import ObjectDetection
import math

#Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("video.mp4")

#initailize count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0

while True: 
    #frame from the video
    ret, frame = cap.read()    #ret is like, if frame finishes we will break/stop
    count += 1
    if not ret:
        break
    
    #Detect objects on frame
    (Class_ids, scroes, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y+ h) / 2)
        center_points_cur_frame.append((cx, cy))
#         print ("FRAME Number",, count, " ", x, y, w, h)
#         cv2.circle (frame, (cx,cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
#     only in the beginning we compare the current and previous frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                
                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:
        
        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()
        
        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
#                 update ids positions
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                    center_points_cur_frame.remove(pt)
                    continue
#                 remove ids lost
            if not object_exists:
                tracking_objects.pop(object_id)
#	add new ids founds
    for pt in center_points_cur_frame:
        
        tracking_objects[track_id] = pt
        track_id += 1
    
    for object_id pt in tracking_objects.items():
        cv2.circle(frame pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
        
    print("Tracking objects")
    print(tracking_objects)
    
    print("CUR FRAME LEFT PTS")
    print (center_points_cur_frame)
    
#     print("PREV Frame")
#     print (center_points_prev_frame)

    cv2.imshow("Frame", frame)
    
#   make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()
    key = cv2.waitKey(0)
    
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


