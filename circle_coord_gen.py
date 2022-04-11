import cv2 as open_cv
import numpy as np

from colors import COLOR_WHITE
from drawing_utils import draw_contours
import json

class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q") #finish creating bounding box

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = open_cv.imread(image).copy()
        self.data = {'coordinates': []}
        self.ids = 0
        self.coordinates = []
        
        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            open_cv.imshow(self.caption, self.image)
            key = open_cv.waitKey(0)      
            json.dump(self.data, self.output, indent=4)      

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):
        radius = 10
        
        if event == open_cv.EVENT_LBUTTONDOWN:
            open_cv.circle(self.image, (x,y), radius, (255,0,0), 2)
            open_cv.imshow(self.caption, self.image)
            self.coordinates.append([x,y,radius])
            # print(self.ids, self.coordinates)
            new_points = {
                'id' : str(self.ids),
                'center': f'({str(self.coordinates[0][0])}, {str(self.coordinates[0][1])})',
                'radius': f'{str(self.coordinates[0][2])}' 
            }
            self.data['coordinates'].append(new_points)
            self.coordinates.pop()
            self.ids += 1
    

        
        
        

        
