import os
import cv2
import numpy as np

def process(img_color):
    #k = -100

    boxes = []
    
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            
    clahe = cv2.createCLAHE(clipLimit =14, tileGridSize = (10,10))
    
    equ = clahe.apply(img)
    
    img = equ
    
    img_copy = img_color
    
    _, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, heirarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    i = cv2.drawContours(img, contours, -1, (255,255,0), 3)
    count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 100000: 
            count += 1
            x,y,w,h = cv2.boundingRect(contour)
            boxes.append((x,y,w,h))

    return boxes
            
            
           
files = ['7d.jpg', 'e0.jpg', 'cb.jpg']
x = {}
y = {}
w = {}
h = {}

for i,f in enumerate(files):
    img = cv2.imread('samples/'+f)
    boxes = process(img)

    x[i] = []
    y[i] = []
    w[i] = []
    h[i] = []
    
    for box in boxes:
        bx,by,bw,bh = box
        
        x[i].append(bx)
        y[i].append(by)
        w[i].append(bw)
        h[i].append(bh)

x = np.array(x)
y = np.array(y)
w = np.array(w)
h = np.array(h)

x.dump('x.pkl')
y.dump('y.pkl')
w.dump('w.pkl')
h.dump('h.pkl')

print x.shape,y.shape,w.shape,h.shape
