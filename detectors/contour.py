import os
import cv2
import numpy

direc = raw_input('Enter directory of files (Include "/" at the end): ')
for f in os.listdir(direc):
    if f.split('.')[-1] == 'JPG ' or f.split('.')[-1] == 'jpg':
        img_color = cv2.imread(direc+f)
        img = cv2.imread(direc+f, cv2.IMREAD_GRAYSCALE)

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
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(img_copy,(x,y),(x+w,y+h), (255,255,0), 3)
                
        cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        cv2.imshow('output', img_copy)
        k  = cv2.waitKey(0) & 0xFF
        
        if k == 27:
            break
        print "[INFO] Countour count: " + str(count)
