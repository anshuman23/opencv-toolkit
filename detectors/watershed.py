import cv2
import numpy as np
import os

direc = raw_input("Enter directory of files (Include '/' at the end): ") 

for f in os.listdir(direc):
    img = cv2.imread(direc+f)
    gray = cv2.imread(direc+f, cv2.IMREAD_GRAYSCALE)

    print "[INFO] Change the kernel [LINE 13] and distance transform code (0.0001 can be changed to 0.1 or 0.001 etc) [LINE 19] to suit your needs if required"
    
    kernel = np.ones((3,3), np.uint8)
    
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,3)
    ret, sure_fg = cv2.threshold(dist_transform,0.0001*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    
    cv2.namedWindow('foreground', cv2.WINDOW_NORMAL)
    cv2.imshow('foreground', sure_fg)
    cv2.waitKey(0)
    
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    
    markers[unknown  == 255] = 0
    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,255,255]
    
    cv2.namedWindow('watershed', cv2.WINDOW_NORMAL)
    cv2.imshow('watershed', img)
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        break
