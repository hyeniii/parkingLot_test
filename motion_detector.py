import cv2 as open_cv
import numpy as np
from matplotlib import pyplot as plt
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE


class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, coordinates, start_frame):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):
        capture = open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame) # start_frame으로 프레임 맞춤

        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data: # for dicts in yaml file
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            rect = open_cv.boundingRect(coordinates) # x,y,w,h
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0] # bounding box x position in respect to origin
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1] # bounding box x,y position in respect to origin
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8), # h, w # black
                [new_coordinates], # white
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8) # rect[3] by rect[2] rectangle 안에 new_coordinates white로 넣기 
            mask = mask == 255 # change to bool array
            self.mask.append(mask)
            logging.debug("mask: %s", self.mask)

        statuses = [False] * len(coordinates_data) # list of falses
        times = [None] * len(coordinates_data)

        while capture.isOpened():
            result, frame = capture.read() # if frame exists (bool), frame pixel (numpy)
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3) # blur image  # img, kernel size, Gaussian kernel standard deviation in X direction (99.7%)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()
            logging.debug("new_frame: %s", new_frame)

            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0 # milisecond to seconds

            for index, c in enumerate(coordinates_data):
                status = self.__apply(grayed, index, c) # True or False

                if times[index] is not None and self.same_status(statuses, index, status): # 
                    print('1', statuses[index], status)
                    times[index] = None
                    continue

                if times[index] is not None and self.status_changed(statuses, index, status): # 
                    print('2', statuses[index], status)
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY: # 1초 이상 동일한 status면 stat 바꿔라
                        statuses[index] = status
                        print('2-1', statuses[index], status)
                        times[index] = None
                    continue

                if times[index] is None and self.status_changed(statuses, index, status): # 
                    print('3',statuses[index], status)
                    times[index] = position_in_seconds
                
                # time[index] is None and self.same_status() -->일 경우 그냥 패스

            for index, p in enumerate(coordinates_data): 
                coordinates = self._coordinates(p)

                #statuses[index] True == green, False == red
                color = COLOR_GREEN if statuses[index] else COLOR_BLUE #blue == red? in open cv?
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            open_cv.imshow(str(self.video), new_frame)
            k = open_cv.waitKey(10)
            if k == ord("q"):
                break
        open_cv.waitKey(10)
        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p) # box coordinate
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index] #box x,y,w,h
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])] # h, w
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        # True == <1.4 // False == >1.4
        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        logging.debug("status: %s", status)

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
