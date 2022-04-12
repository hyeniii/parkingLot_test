import cv2
import numpy as np
from circle_coord_gen import CoordinatesGenerator
from colors import *
import json

img_file = 'images/parking_lot_2.png'
vid_file = 'videos/parking_lot_2.mp4'
data_file = 'data/coodinates.json'

class CaptureReadError(Exception):
    pass

if img_file is not None:
    with open(data_file, 'w+') as points:
        generator = CoordinatesGenerator(img_file, points, COLOR_RED)
        generator.generate()
        
    with open(data_file, 'r') as data:
        points = json.load(data)
        capture = cv2.VideoCapture(vid_file)
        capture.set(cv2.CAP_PROP_POS_FRAMES, 400)
        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))
            
            new_frame = frame.copy()
            for i in points['coordinates']:
                new_frame = cv2.circle(new_frame, (i['center_x'], i['center_y']), i['radius'], (0,0,255), 2)
                new_frame = cv2.putText(new_frame, str(i['id'] + 1), (i['center_x'], i['center_y'],), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 2)
                
            cv2.imshow('parking_lot', new_frame)
            k = cv2.waitKey(10)
            if k == ord("q"):
                break
        cv2.waitKey(10)
        capture.release()
        cv2.destroyAllWindows()
