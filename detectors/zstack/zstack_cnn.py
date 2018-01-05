import cv2
import os
import numpy as np
import keras
from keras.models import load_model

X_large = []
names = []
paths = []

row = 128
col = 128
wbcs = 0
nothing = 0

model = load_model('model.h5')

files = os.listdir('focussed/')
for field in files:
    for image in os.listdir('focussed/'+field):
        img = cv2.imread('focussed/'+field+'/'+image)
        h,w,_ = img.shape
        padded_img = np.zeros((row, col, 3), np.uint8)
        if img.shape[1] < col and img.shape[0] < row:
            padded_img[0:h, 0:w] = img
        else :
            if h > w :
                img = cv2.resize(img, (int(col * w / h), row))
                padded_img[0:row, 0:int(col * w / h)] = img
            else:
                img = cv2.resize(img, (col, int(row * h / w)))
                padded_img[0:int(row * h / w), 0:col] = img
                
        X_large.append(padded_img)
        names.append(image)
        paths.append('focussed/'+field+'/'+image)
        
X_large = np.array(X_large)

X = np.zeros([X_large.shape[0],32,32,3])

for idx,im in enumerate(X_large):
    ratio = 32.0/im.shape[1]
    dim = (32, int(im.shape[0] * ratio))
    im_resized = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
    X[idx] = im_resized
    
print X.shape

dtype_mult = 255.0
X = X.astype('float32')/dtype_mult

pred = model.predict(X)

for idx in range(pred.shape[0]):
    if pred.argmax(axis = 1)[idx] == 0:
        wbcs += 1
        img = cv2.imread(paths[idx])
        cv2.imwrite('cnn-outputs/wbc-'+names[idx], img)
        
    elif pred.argmax(axis = 1)[idx] == 1:
        nothing += 1
        img = cv2.imread(paths[idx])
        cv2.imwrite('cnn-outputs/notwbc-'+names[idx], img)

print wbcs, nothing
