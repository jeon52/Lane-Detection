import cv2
import numpy as np

original = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/train/0a0a0b1a-7c39d841.jpg')
#file 3, has lanes, but use colormaps
lanes = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-3/labels/lane/colormaps/train/0a0a0b1a-7c39d841.png')
#file 2 has drivable area
drivable = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-2/labels/drivable/colormaps/train/0a0a0b1a-7c39d841.png')

#dimension of the original image - Note that all images (lane, drivable) related to this original image shares same dimension
(H1, W1, C1) = original.shape

#create new image file
newimage = np.empty([H1, W1, 3], np.uint8)

# change pixels on the original image if the lane and drivable has some pixel value not black (255, places significant)
# 0 represents black, 255 represents white 
for i in range(H1): #0 to height - 1
        for j in range(W1): #0 to width - 1
            for k in range(C1): #0 to channel -1
                if lanes[i][j][k] != 0:
                        original[i][j][k] = 0
                        drivable[i][j][k] = 0
                if drivable[i][j][k] != 0:
                        original[i][j][k] = 0

for i in range(H1): #0 to height - 1
        for j in range(W1): #0 to width - 1
            for k in range(C1): #0 to channel -1
                newimage[i][j][k] = original[i][j][k] + lanes[i][j][k] + drivable[i][j][k]

#show the new image
cv2.imshow('overlayed image', newimage)

#kills the image when any button is pressed:
cv2.waitKey(0)
cv2.destroyAllWindows()

#TO DO LIST:
#need to add boxes
#need to go through everysingle images on the folder
#need to download all these folders created into a separate folder
