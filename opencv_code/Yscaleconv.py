#Uses OpenCV to process image
import cv2

#reads color image 
#put any image that you would like to process below:
RGB = cv2.imread('/Users/bradjeon/Downloads/exampleimage.jpg')
#converts color image to Y scale image
#automatically calculates 0.2162(R) + 0.7152(G) + 0.0722(B)
Y = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

#shows the images with name
cv2.imshow('RBG image',RGB)
cv2.imshow('Yscale image', Y)

#kills the image when any button is pressed:
#Note this is not optional
cv2.waitKey(0)
cv2.destroyAllWindows()
