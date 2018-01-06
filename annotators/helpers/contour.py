import os
import cv2
import numpy

def process(img):

    bbs = []

    img_color = img
    img = cv2.cvtColor(img, cv2.BGR2GRAY)
    
    print "[INFO] If not working well for your image, consider changing the below line to better suit your needs: Play around with clipLimit between 14 and 44 (10 value intervals) and tileGridSize between 10,10 to 80,80 (20 or 10 spaced intervals) [LINE 14]"
    print "[INFO] If not working well for your image, consider removing the contourArea condition below or changing it to detect contours of the size you want [LINE 28]"
    
    clahe = cv2.createCLAHE(clipLimit =14, tileGridSize = (10,10))
    
    equ = clahe.apply(img)
    
    img = equ
    
    img_copy = img_color

    _, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    im, contours, heirarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    i = cv2.drawContours(img, contours, -1, (255,255,0), 3)
    count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 100000: 
            count += 1
            bbs.append((x,y,w,h))
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(img_copy,(x,y),(x+w,y+h), (255,255,0), 3)
        
    print "[INFO] Countour count: " + str(count)
    return np.array(bbs)    
