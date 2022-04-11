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