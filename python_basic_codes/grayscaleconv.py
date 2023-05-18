#Will be using different 
import cv2
import numpy as np

#reads color image and split into 3 different channels 
RGB = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/test/cabc30fc-e7726578.jpg')

#get dimensions of the image
height = RGB.shape[0]
width = RGB.shape[1]
channels = RGB.shape[2]

#or 

(H, W, C) = RGB.shape
print("height is ", H, height)
print("width is ", W, width)
print("channel is ", C, channels)

#creating a new blank image using numpy
grayimage = np.empty([height, width], np.uint8)

#get pixel values of an image and multiply the BT709 constants
for i in range(height): #0 to height - 1
        for j in range(width): #0 to width - 1
            grayimage[i][j] = (RGB[i][j][0]*0.2126 + RGB[i][j][1]*0.7152 + RGB[i][j][2] * 0.0722)

#lets compare with grayscale image made from opencv function
Y = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

#show the new grayscale image
cv2.imshow('grayscale image', grayimage)
cv2.imshow('grayscale image made from opencv', Y)

#kills the image when any button is pressed:
#Note this is not optional
cv2.waitKey(0)
cv2.destroyAllWindows()