import cv2
import os
import numpy as np

print "[INFO] Change the size of the grid square according to your requirements [LINE 6]"
grid_size = 208 

k = -100

yes_blocks = []
no_blocks = []

direc = raw_input('Enter directory of files (Include "/" at the end): ') 
    
for idx,f in enumerate(os.listdir(direc)):
    img_color = cv2.imread(direc + f)
    img = cv2.imread(direc + f, cv2.IMREAD_GRAYSCALE)
    img = img[480:1520, 420:1460]
    img_color = img_color[480:1520, 420:1460, :]
    img_copy = np.copy(img_color)
    
    cv2.namedWindow('FIELD', cv2.WINDOW_NORMAL)
    
    print idx 
    for y in range(0,1040,grid_size): ## TODO: Custom image resizing required. 1040 [(1520-480) or (1460-420)] is not correct
        for x in range(0,1040,grid_size): ## TODO: Custom image resizing required. 1040 [(1520-480) or (1460-420)] is not correct
            
            img_copy = cv2.rectangle(img_color,(y,x), (y+grid_size, x+grid_size), (255,0,255), 2)
            
            cv2.imshow('FIELD',img_copy)
            k = cv2.waitKey(0) & 0xFF
            
            if k == 121:
                img_crop = img[x:(x+grid_size), y:(y+grid_size)]
                yes_blocks.append(img_crop)
                
            elif k == 110:
                img_crop = img[x:(x+grid_size), y:(y+grid_size)]
                no_blocks.append(img_crop)
                
            elif k == 100:
                continue

            elif k == 27:
                break

        if k == 27:
            break

    if k == 27:
        break

np.array(yes_blocks).dump('yes.pkl')
np.array(no_blocks).dump('no.pkl')
