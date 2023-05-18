#Converting an image to Y scale image. 
import cv2
RGB = cv2.imread('/Users/bradjeon/Downloads/exampleimage.jpg')
Y = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

#To set a threshold value use the following command
#for values smaller or equal to threshold value -> 255, and bigger -> 0
#cv2.threshold(image name, threshold value, output value, cv2.THRESH_BINARY)
#do not forget the T in the left side of the equation - represents Threshold value 
(T,thresholdimageinv) = cv2.threshold(Y, 160, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("image", thresholdimageinv)

#kill window when any button pressed
cv2.waitKey(0)
cv2.destroyAllWindows()