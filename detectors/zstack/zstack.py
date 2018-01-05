import os
import pickle
import cv2
import numpy as np
from collections import defaultdict

k = -100


#for s in ['0M1512325096874', '0M1512334404894', '0M1512336187719', '0M1512347237847', '0M1512349078447']:
#    for f in os.listdir('/home/anshuman/coding_practice/morphle/Apollo-Urine-Samples/Good-WBC/'+s+'/'):
#for s in ['0M1512327891843', '0M1512333541399', '0M1512335324615', '0M1512337126841']:
#    for f in os.listdir('/home/anshuman/coding_practice/morphle/Apollo-Urine-Samples/Maybe/'+s+'/'):
for s in range(1):
    for f in os.listdir('more-samples/'):
    #for f in ['X45p0Y15p0Z0p0F1.JPG']:
        d = {}
        results = {}

        if f.split('.')[-1] == 'JPG' or f.split('.')[-1] == 'jpg':
            #img_color = cv2.imread('/home/anshuman/coding_practice/morphle/Apollo-Urine-Samples/Maybe/'+s+'/'+f)
            img_color = cv2.imread('more-samples/'+f)
            img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            
            #img_color = image
            #img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            
            clahe = cv2.createCLAHE(clipLimit =14, tileGridSize = (10,10))
            
            equ = clahe.apply(img)
            
            img = equ
            
            img_copy = np.copy(img_color)
            
            
            _, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            #im, contours, heirarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours, heirarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            i = cv2.drawContours(img, contours, -1, (255,255,0), 3)
            count = 0
            valid_contours = []
            for contour in contours:
                if cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 100000: 
                    #epsilon = 0.01*cv2.arcLength(contour, True)
                    #contour = cv2.approxPolyDP(contour, epsilon, True)
                    count += 1
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(img_copy,(x,y),(x+w,y+h), (255,255,0), 3)
                    (cx,cy), r = cv2.minEnclosingCircle(contour)
                    valid_contours.append((x,y,w,h,cx,cy,r))
                    #d[(x,y,w,h)] = []

            
            for c in valid_contours:
                min_dist = 10000000
                for n in valid_contours:
                    #c = (x,y,w,h)
                    #n = (nx,ny,nw,nh)
                    #c = (x,y,w,h,cx,cy,r)
                    #n = (nx,ny,nw,nh,ncx,ncy,nr)

                    #if not(c == n) and (np.square(cx-ncx) + np.square(cy-ncy)) < np.square(1.5*r):
                    if not c == n and ((np.square(c[4]-n[4]) + np.square(c[5]-n[5])) < min_dist):
                        d[c] = n
                        min_dist = np.square(c[4]-n[4]) + np.square(c[5]-n[5])

            print len(d)
            
            for k,v in d.iteritems():
                #im = np.copy(img_color)
                #cv2.rectangle(im, (k[0],k[1]), (k[0]+k[2], k[1]+k[3]), (0,0,255), 3)
                ##for val in v:
                ##    cv2.rectangle(im, (val[0],val[1]), (val[0]+val[2], val[1]+val[3]), (0,255,255),3)
                #cv2.rectangle(im, (v[0],v[1]), (v[0]+v[2], v[1]+v[3]), (0,255,255), 3) 
                
                #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
                #cv2.imshow('output', im)
                #k  = cv2.waitKey(0) & 0xFF


                if (k[4] - v[4]) == 0:
                    slope = 100000000000000000
                else:
                    slope = (k[5] - v[5])/(k[4] - v[4])

                    
                dist = np.square(k[4] - v[4]) + np.square(k[5] - v[5])

                results[k] = (v,slope,dist)

            print len(results)
                
                        
            cv2.namedWindow('output', cv2.WINDOW_NORMAL)
            cv2.imshow('output', img_copy)
            k  = cv2.waitKey(0) & 0xFF
            
            if k == 97:
                output = open(f.split('.')[0]+'.pkl', 'wb')
                pickle.dump(results, output)
                output.close()
                #cv2.imwrite('output-'+f,img_copy)
                
                
            elif k == 27:
                break
            
            #print count
            

    if k == 27:
        break

'''
# read python dict back from the file
pkl_file = open('myfile.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()
'''
