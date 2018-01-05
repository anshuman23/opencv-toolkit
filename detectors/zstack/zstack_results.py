import pickle
import numpy as np
import cv2
from random import randint
import os

relations = {}
check = {}

def lapla(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    clipped = np.clip(laplacian, 0, None)
    squared = clipped
    return np.sum(squared)


files = os.listdir('more-samples/')
iterations = sorted([int(f.split('.')[0].split('F')[-1]) for f in files])

iterations1 = sorted([int(f.split('.')[0].split('F')[-1]) for f in files])
iterations2 = sorted([int(f.split('.')[0].split('F')[-1]) for f in files])

iterations1 = iterations1[0:-1]
iterations2 = iterations2[1:]

print iterations1
print iterations2

name = files[0].split('.')[0].split('F')[0]

for idx,(it1,it2) in enumerate(zip(iterations1, iterations2)):
    first = name+'F'+str(it1)+'.pkl'
    second = name+'F'+str(it2)+'.pkl'
    
    f = open(first, 'rb')
    dic1 = pickle.load(f)
    f.close()
    
    f = open(second, 'rb')
    dic2 = pickle.load(f)
    f.close()
    
    
    need = {}

    relations[idx] = []
    
    print len(dic1)
    print len(dic2)

    for k1,v1 in dic1.iteritems():
        slope = v1[1]
        dist = v1[2]
        #print slope,dist
        #print "----------"

        wx = k1[0] - 2 
        wy = k1[1] - 2
        ww = k1[2] + 2
        wh = k1[3] + 2

        mind = 100000
        for k2,v2 in dic2.iteritems():
            s = v2[1]
            d = v2[2]
            #print s,d
            if wx < (k2[0]+k2[2]/2) and (k2[0]+k2[2]/2) < (wx + ww) and wy < (k2[1]+k2[3]/2) and (k2[1]+k2[3]/2) < (wy + wh):
                #if wx < k2[2] and k2[2] < (wx + ww) and wy < k2[3] and k2[3] < (wy + wh):
                #print "yes"
                if (np.abs(s-slope) + np.abs(d-dist)) < mind:
                    mind = (np.abs(s-slope) + np.abs(d-dist))
                    need[k1] = k2
                    
                    break

        relations[idx].append((k1,k2))
        check[k1] = True
        check[k2] = True

                    
                
    print len(need)


    image1 = cv2.imread('more-samples/'+first.split('.')[0]+'.JPG')
    image2 = cv2.imread('more-samples/'+second.split('.')[0]+'.JPG')


    for i,(k,v) in enumerate(need.iteritems()):
        
        img1 = np.copy(image1)
        img2 = np.copy(image2)
        cv2.rectangle(img1, (k[0],k[1]), (k[0]+k[2],k[1]+k[3]), (0,0,255),3)
        cv2.rectangle(img2, (v[0],v[1]), (v[0]+v[2],v[1]+v[3]), (0,0,255),3)
        res = np.hstack((img1,img2))
        cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        cv2.imshow('output', res)
        k = cv2.waitKey(0) & 0xFF
        if k == 97:
            cv2.imwrite('output-images/'+str(i)+'.jpg', res)
        if k == 27:
            break


for i in range(len(iterations1)):
    first = name+'F'+str(iterations[i])+'.JPG'
    second = name+'F'+str(iterations[i+1])+'.JPG'
    
    imgf = cv2.imread('more-samples/'+ first)
    imgs = cv2.imread('more-samples/'+ second)

    os.system('mkdir focussed/F'+str(iterations[i]))
    
    for (k1,k2) in relations[i]:
        if check[k1] == True:
            img1 = np.copy(imgf)
            img2 = np.copy(imgs)
            
            img1 = img1[k1[1]:k1[1]+k1[3], k1[0]:k1[0]+k1[2]]
            img2 = img2[k2[1]:k2[1]+k2[3], k2[0]:k2[0]+k2[2]]

            l1 = lapla(img1)
            l2 = lapla(img2)

            if l1 > l2:
                cv2.imwrite('focussed/F'+str(iterations[i])+'/'+first.split('.')[0]+'-'+str(k1[0])+'-'+str(k1[1])+'-'+str(k1[2])+'-'+str(k1[3])+'.jpg', img1)
                check[k2] = False
                continue
            elif l2 > l1:
                continue

os.system('mkdir focussed/F'+str(iterations[-1]))
for (k1,k2) in relations[len(iterations1)-1]:
    image_name = name+'F'+str(iterations[-1])+'.JPG'
    image = cv2.imread('more-samples/'+ image_name)
    if check[k2] == True:
        img = np.copy(image)
        img2 = img[k2[1]:k2[1]+k2[3], k2[0]:k2[0]+k2[2]]
        cv2.imwrite('focussed/F'+str(iterations[-1])+'/'+image_name.split('.')[0]+'-'+str(k2[0])+'-'+str(k2[1])+'-'+str(k2[2])+'-'+str(k2[3])+'.jpg', img2)
        check[k2] = False
        continue
