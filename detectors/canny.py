import cv2
import numpy as np
import os

def update(x):
    pass

cv2.namedWindow('FIELD', cv2.WINDOW_NORMAL)

cv2.createTrackbar('t1','FIELD',0,255, update)
cv2.createTrackbar('t2','FIELD',0,255, update) 

direc = raw_input("Enter directory of files (Include '/' at the end): ")

k = -100

for f in os.listdir(direc):

    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        image = cv2.imread(direc+f, cv2.IMREAD_GRAYSCALE)
        image = cv2.bilateralFilter(image, 5, 175, 175)               
        t1 = cv2.getTrackbarPos('t1', 'FIELD')
        t2 = cv2.getTrackbarPos('t2', 'FIELD')
    
        canny = cv2.Canny(image,t1,t2)
        
        h,w = image.shape
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max(10, int(0.01*h + 1)), max(10, int(0.01*h +1))))
        canny = cv2.morphologyEx(canny, cv2.MORPH_DILATE, kernel)
        im2,contours, heirarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(image, contours, -1, (0,255,0),3)
        
        image = cv2.resize(image, (1920,1080))
        cv2.imshow('FIELD', image)

        if k == 99:
            break


    if k == 27:
        break

    elif k == 99:
        continue
