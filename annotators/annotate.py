import cv2
import numpy as np
import os
from segment2 import return_bbs
from collections import defaultdict

######################## *///*******RULES********\\\* #####################
#1 In a double bounding boxed rbc let the inner box also be labeled as rbc
#2 Only say not rbc to really small inside boxes
#3 Do not make labelings so as to confuse the CNN
################### *///*******BEST-OF-LUCK!********\\\* ##################

k = -100

global selected
selected = {}
selected = defaultdict(lambda:False,selected) 

global truec
truec = {}
truec = defaultdict(lambda:0,truec) 

global state
state = 2 # 0 => GOOD RBC, 1 => BAD RBC, 2 => NOT RBC 

def select(event, x, y, flags, param):
    global bbs, truec, state, selected
    
    if event == cv2.EVENT_LBUTTONDOWN:
        for (bx,by,bw,bh) in bbs:
            if bx < x and x < (bx + bw) and by < y and y < (by + bh):
                if selected[(bx,by,bw,bh)]:
                    selected[(bx,by,bw,bh)] = False
                    truec[(bx,by,bw,bh)] = 0
                    cv2.rectangle(imagec, (bx,by), (bx+bw, by+bh), (0,0,255), 3)
                    cv2.imshow("annotate", imagec)

                else:
                    selected[(bx,by,bw,bh)] = True
                    truec[(bx,by,bw,bh)] = state
              
                    if state == 2:
                        cv2.rectangle(imagec, (bx,by), (bx+bw, by+bh), (0,255,0), 3)
                        cv2.imshow("annotate", imagec)
                    elif state == 1:
                        cv2.rectangle(imagec, (bx,by), (bx+bw, by+bh), (255,0,0), 3)
                        cv2.imshow("annotate", imagec)
                    
direc = '/home/anshuman/coding_practice/Blood-Images-Dataset/Metropolis-Blood/'
store = '/home/anshuman/coding_practice/morphle/Blood/Classification/'
good_rbc = store+'good_rbc/'
bad_rbc = store+'bad_rbc/'
not_rbc = store+'not_rbc/'


for s in os.listdir(direc):
    for f in os.listdir(direc+s):
        print direc+s+'/'+f
        counter = 0
        global bbs, truec, state, selected

        state = 2
        
        bbs = np.array([])
        image = cv2.imread(direc+s+'/'+f)
        imagec = np.copy(image)
        imagecc = np.copy(imagec)

        bbs = return_bbs(image)

        for _ in range(2):
            for (x,y,w,h) in bbs:
                cv2.rectangle(imagec, (x,y), (x+w, y+h), (0,0,255),3)
            
            cv2.namedWindow("annotate", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("annotate", select)
            cv2.imshow("annotate", imagec)
            k = cv2.waitKey(0) & 0xFF

            selected = {}
            selected = defaultdict(lambda:False,selected) 
            
            if k == 110: #NEXT
                print "NEXT"
                state -= 1
                continue
            
            if k == 27: #EXIT
                break

            if k == 115: #SKIP
                break

        if k == 115:
            truec = {}
            truec = defaultdict(lambda:0,truec)
            continue
        
            
        for (kx,ky,kw,kh) in bbs:
            image_crop = np.copy(imagecc)
            counter += 1
            
            if truec[(kx,ky,kw,kh)] == 0:
                image_crop = image_crop[ ky:(ky+kh), kx:(kx+kw)]
                cv2.imwrite(good_rbc+str(counter)+'-'+s+'$'+f, image_crop)

            elif truec[(kx,ky,kw,kh)] == 1:
                image_crop = image_crop[ky:(ky+kh), kx:(kx+kw)]
                cv2.imwrite(bad_rbc+str(counter)+'-'+s+'$'+f, image_crop)

            elif truec[(kx,ky,kw,kh)] == 2:
                image_crop = image_crop[ky:(ky+kh), kx:(kx+kw)]
                cv2.imwrite(not_rbc+str(counter)+'-'+s+'$'+f, image_crop)

        truec = {}
        truec = defaultdict(lambda:0,truec)
                
        if k == 27:
            break
    if k == 27:
        break

print str(counter)
