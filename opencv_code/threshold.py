#Converting an image to Y scale image. 
import cv2
RGB = cv2.imread('/Users/bradjeon/Downloads/exampleimage.jpg')
Y = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

#To set a threshold value use the following command
#values lower and equal to threshold value will be set to 0 while values bigger than threshold value will be set to output value.
#cv2.threshold(image name, threshold value, output value, cv2.THRESH_BINARY)
(T,thresholdimage) = cv2.threshold(Y, 160, 255, cv2.THRESH_BINARY)
cv2.imshow("image", thresholdimage)

#kill window when any button pressed
cv2.waitKey(0)
cv2.destroyAllWindows()