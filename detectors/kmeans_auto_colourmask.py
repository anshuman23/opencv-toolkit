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

    print "[INFO] Change number of clusters to reflect the number of dominant colours you want to be found [LINE 17]"
    print "[INFO] Can also change range of colour mask applied from centroid/dominant colour [LINE 25 and LINE 26]"
    
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
