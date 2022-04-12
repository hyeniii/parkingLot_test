import cv2
import numpy as np
from circle_coord_gen import CoordinatesGenerator
from colors import *
import json

img_file = 'images/parking_lot_2.png'
vid_file = 'videos/parking_lot_2.mp4'
data_file = 'data/coodinates.json'


if img_file is not None:
    with open(data_file, 'w+') as points:
        generator = CoordinatesGenerator(img_file, points, COLOR_RED)
        generator.generate()
        
    with open(data_file, 'r') as data:
        points = json.load(data)
        img = cv2.imread(img_file).copy()
        for i in points['coordinates']:
            img = cv2.circle(img, (i['center_x'], i['center_y']), i['radius'], (0,0,255), 2)
            img = cv2.putText(img, str(i['id'] + 1), (i['center_x'], i['center_y'],), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 2)
        
        cv2.imshow('parking lot', img)
        cv2.waitKey(0)