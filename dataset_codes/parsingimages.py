import os
import cv2
import json
import numpy as np

#required string for calling cv2.imshow
slash = '/'

#create example image and get resolution of an image that will be used
example = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/train/0a0a0b1a-7c39d841.jpg')
(H1, W1, C1) = example.shape

#create new blank image with 3 channels using numpy
newimage = np.empty([H1, W1, 3], np.uint8)

#create path for the folder which contains all the images
originaldirectory = '/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/train'
lanedirectory = '/Users/bradjeon/dataset/Dataset_Updates/bdd100k-3/labels/lane/colormaps/train'
drivabledirectory = '/Users/bradjeon/dataset/Dataset_Updates/bdd100k-2/labels/drivable/colormaps/train'

#read json file for names of the images
with open('/Users/bradjeon/dataset/Dataset_Updates/bdd100k/labels/det_20/det_train.json', "r") as JsonFile:
    read_json = json.load(JsonFile) 
    for dictionary in read_json:
        namesjpg = dictionary['name'] #get names from the json file
        nameswithoutextension = (os.path.splitext(namesjpg)[0]) #creating a name with no extension
        namespng = nameswithoutextension + ".png" #creating a string with .png extension
        for original in os.listdir(originaldirectory):
           if original == namesjpg:
               originalname = original
        for lane in os.listdir(lanedirectory):
            if lane == namespng:
                lanename = lane
        for drivable in os.listdir(drivabledirectory):
            if drivable == namespng:
                drivablename = drivable  
                print (drivablename)

        #calling each images using opencv      
        originalimage = cv2.imread(originaldirectory + slash + originalname)
        laneimage = cv2.imread(lanedirectory + slash + lanename)
        drivableimage = cv2.imread(drivabledirectory + slash + drivablename)

        # 0 represents black, 255 represents white 
        for i in range(H1): #0 to height - 1
            for j in range(W1): #0 to width - 1
              for k in range(C1): #0 to channel -1
                if laneimage[i][j][k] != 0:
                        originalimage[i][j][k] = 0
                        drivableimage[i][j][k] = 0
                if drivableimage[i][j][k] != 0:
                        originalimage[i][j][k] = 0

        cv2.imshow('originalimage', originalimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        for i in range(H1): #0 to height - 1    
            for j in range(W1): #0 to width - 1
                for k in range(C1): #0 to channel -1
                    newimage[i][j][k] = originalimage[i][j][k] + laneimage[i][j][k] + drivableimage[i][j][k]

        #show the new image
        cv2.imshow('overlayed image', newimage)

        #kills the image when any button is pressed:
        cv2.waitKey(0)
        cv2.destroyAllWindows()