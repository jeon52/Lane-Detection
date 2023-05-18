import json
import cv2
import numpy as np

#pull up an image from the dataset, check its dimensions
example = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/train/0a0a0b1a-7c39d841.jpg')
(H1, W1, C1) = example.shape

#create a new image with same dimensions
newimage = np.empty([H1, W1, C1], np.uint8)

#open the json file
with open('/Users/bradjeon/dataset/Dataset_Updates/bdd100k/labels/det_20/det_train.json', "r") as JsonFile:
    #changes into python object and make it readable
    read_json = json.load(JsonFile) 
    for dictionaries in read_json:
        namesjpg = dictionaries['name'] #gets the name of the image that is being used 
        labels = dictionaries['labels'] #goes into "labels" section of the json file 
        for box2d in labels:
            xy = box2d['box2d']
            x1 = xy['x1'] 
            x2 = xy['x2']
            y1 = xy['y1']
            y2 = xy['y2']

            # make 4 coordinates #can they be decimal values??
            x1y1 = [x1, y1]
            x1y2 = [x1, y2]
            x2y1 = [x2, y1]
            x2y2 = [x2, y2]

                #for loop to make lines between these coordinates 
                #(x1:x2, y1:y2, :)

                # modify all 3 channels 
                # Need to call original image, lanes, and drivable image as well. 



                

