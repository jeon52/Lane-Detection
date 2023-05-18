#import cv
import cv2
#matplotlib is required to plot a histogram
from matplotlib import pyplot as plt

#reads color image
RGB = cv2.imread('/Users/bradjeon/Downloads/exampleimage.jpg')

#conversion to Yscale image
Y = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

#prepares histogram for Yscale image to be plotted
#cv.calcHist(image name, channels, mask, bin size, ranges)
# range = range of pixel values
# bin size = width value per bin
# mask = just put None 
Yhist = cv2.calcHist([Y], [0], None, [256], [0,256])

#set x axis, y axis, name and plots the prepared histogram information
plt.figure() #creates a new figure
plt.title("Histogram")
plt.xlabel("range")
plt.ylabel("# of Pixels")
plt.plot(Yhist) #plots the histogram values

#displays figure
plt.show()