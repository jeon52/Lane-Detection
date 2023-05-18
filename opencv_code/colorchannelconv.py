#import CV
import cv2

#read original color image
RGB = cv2.imread('/Users/bradjeon/Downloads/exampleimage.jpg')

#this equations calculates each RBG color channel of the image 
#automatically calculates 0.2162(R) + 0.7152(G) + 0.0722(B)
#must be in B G R order
(B,G,R) = cv2.split(RGB)

#show the color channel and original image
cv2.imshow('Original RGB image',RGB)
cv2.imshow('Blue image', B)
cv2.imshow('Green image', G)
cv2.imshow('Red image', R)

#make a new color image
newRGB = cv2.merge([B,G,R])

#show new color image
cv2.imshow('New RGB image', newRGB)

#kills the image when any button is pressed:
#Note this is required
cv2.waitKey(0)
cv2.destroyAllWindows()
