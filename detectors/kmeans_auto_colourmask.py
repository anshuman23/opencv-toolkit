import cv2
import numpy as np
import os
from sklearn.cluster import KMeans

direc = raw_input("Enter directory of files (Include '/' at the end): ") 

for f in os.listdir(direc):
    image = cv2.imread(direc+f)
    image_copy = np.copy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    print "[INFO] Change number of clusters to reflect the number of dominant colours you want to be found"
    
    clt = KMeans(n_clusters = 2)
    clt.fit(image)
    
    centroids = clt.cluster_centers_
    centroids = centroids.astype('uint8').tolist()
    
    image = image_copy
    color = centroids[0] 
    lower = np.array([color[2]-10, color[1]-10, color[0]-10])
    upper = np.array([color[2]+10, color[1]+10, color[0]+10])
    mask = cv2.inRange(image, lower, upper)

    image = cv2.bitwise_and(image, image, mask = mask)
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.imshow('mask', image)
    k = cv2.waitKey(0) & 0xFF

    if k == 27:
        break

'''
img = cv2.imread('image_150310_008.JPG')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
gray = cv2.imread('image_150310_008.JPG', cv2.IMREAD_GRAYSCALE)
kernel = np.ones((3,3), np.uint8)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,3)
ret, sure_fg = cv2.threshold(dist_transform,0.0001*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
cv2.namedWindow('watershed', cv2.WINDOW_NORMAL)
cv2.imshow('watershed', sure_fg)
cv2.waitKey(0)

unknown = cv2.subtract(sure_bg,sure_fg)

ret, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1

markers[unknown  == 255] = 0
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,255,255]

cv2.namedWindow('watershed', cv2.WINDOW_NORMAL)
cv2.imshow('watershed', img)
cv2.waitKey(0)
