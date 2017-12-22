import cv2
import numpy as np
import imutils
from imutils import face_utils
import dlib
import os

k = -100

direc = raw_input("Enter directory of images (Include '/' at the end): ")

for f in os.listdir(direc):
    img_color = cv2.imread(direc+f)
    img = cv2.imread(direc+f, cv2.IMREAD_GRAYSCALE)
    print img.shape
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        
    detected = detector(img, 1)
        
    for i, detect in enumerate(detected):
        print "processing..."
        shape = predictor(img, detect)
        shape = face_utils.shape_to_np(shape)
        
        for (name, (i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            print i,j, name
            x,y,w,h = cv2.boundingRect(np.array([shape[i:j]]))
            output = img_color[x:x+w, y:y+h]    
            cv2.imshow("output", output)
            k = cv2.waitKey(0) & 0xFF
                
                

