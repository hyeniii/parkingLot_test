from fileinput import filename
import cv2
import numpy as np

path = '/home/nicole/propwave/ParkingLot/parking_lot/images/parking_lot_2.png'

img = cv2.imread(filename = path)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

boundaries = [([0,0,100],[255,50,225]), #white
              ([20,100,100], [30,255,255])  #yellow
              ]
for (lower, upper) in boundaries:
    lower = np.array(lower, dtype= 'uint8')
    upper = np.array(upper, dtype= 'uint8')
    mask = cv2.inRange(hsv_img, lower, upper)
    cv2.imshow('parking_lot',mask)
    cv2.waitKey() 
    cv2.destroyAllWindows() 

 
 
# line_image = np.copy(img) * 0
# gray = cv2.cvtColor(src=img, code = cv2.COLOR_BGR2GRAY)
# blur_gray = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)
# edges = cv2.Canny(image=blur_gray, threshold1=50, threshold2=150, apertureSize=3)
# lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=30, maxLineGap=5)
# for i in range(len(lines)):
#     for x1,y1,x2,y2 in lines[i]:
#         cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

# lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)



