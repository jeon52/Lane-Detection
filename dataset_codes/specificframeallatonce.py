import os
import numpy as np
import cv2
import json
import matplotlib
import matplotlib.pyplot as plt

hostip = "128.32.162.150" #bdd100k Server IP address
hostname = "http://dl.yf.io/bdd100k/videos/" #address of where all the videos are located #change this 
#https://www.yf.io/#services or http://dl.yf.io/bdd100k/videos/
ext = ".mov" #extension for videos in the website
response = os.system("ping -c 1 128.32.162.150") 

#and then check the response...
if response == 0: #response is back successfully
  print (hostip, 'the website is up!')

  #get name using json
  with open('/Users/bradjeon/dataset/Dataset_Updates/bdd100k/labels/det_20/det_val.json', "r") as JsonFile:
    read_json = json.load(JsonFile) 
    for dictionary in read_json:
      namesjpg = dictionary['name'] #get names from the json file
      nameswithoutextension = (os.path.splitext(namesjpg)[0]) #creating a name with no extension
      videowithext = nameswithoutextension + ext #creating a string with .mov extension
      print(videowithext)

      #load video from the website
      video = cv2.VideoCapture(hostname + videowithext)
      if video.isOpened() is None: #if the video is not loaded
        print (video, "video cannot be loaded")

      fps = video.get(cv2.CAP_PROP_FPS) #gets frames per second of the video
      print("fps", fps)

      startingpoint = round(fps * 5) #checked with the original dataset!!! matches!!!
      #do not do int(fps * 10) or int(fps * 10) - 1 - this will only round down!!!
      i = 0 #initialization
      image_array = [] #create a list which accepts multiple image frames. 

      for i in range (12):
        if i == 11: #make sure i does not go over 10
          video.release()
          break
        sequentialpoint = startingpoint + round(fps * 10 + i) #starts from default 0 therefore, the video starts at 5 seconds
        # 5 frames before and 5 frames after:
        video.set(cv2.CAP_PROP_POS_FRAMES, sequentialpoint)
        ret, frame = video.read() #frame is the starting frame
        if ret == True:
          image_array.append(frame)
          print("Inserted to the list", i + 5, "Seconds")
    
      #lets make a figure ~
      #fig = plt.figure(figsize = (10,10)) #figure size is in inches - what happens if we decrease the size? - not much change lol
      #plt.title("Frames from 5 seconds to 15 seconds")
      #plt.axis('off')
      #rows = 2
      #cols = 6
    
      #place images into variables
      Image5sec = image_array[0]
      Image6sec = image_array[1]
      Image7sec = image_array[2]
      Image8sec = image_array[3]
      Image9sec = image_array[4]
      Image10sec = image_array[5]
      Image11sec = image_array[6]
      Image12sec = image_array[7]
      Image13sec = image_array[8]
      Image14sec = image_array[9]
      Image15sec = image_array[10]

      #place images into the figure
      cv2.imshow(" 5 frames before ", Image5sec) 
      cv2.imshow(" 4 frames before ", Image6sec) 
      cv2.imshow(" 3 frames before ", Image7sec) 
      cv2.imshow(" 2 frames before ", Image8sec)
      cv2.imshow(" 1 frames before ", Image9sec)
      cv2.imshow(" 10 second point ", Image10sec)
      cv2.imshow(" 1 frames after ", Image11sec)
      cv2.imshow(" 2 frames after ", Image12sec)
      cv2.imshow(" 3 frames after ", Image13sec) 
      cv2.imshow(" 4 frames after ", Image14sec)
      cv2.imshow(" 5 frames after ", Image15sec)

      cv2.waitKey(0)
      cv2.destroyAllWindows() 


else: #response not back 
  print (hostip, 'the website is down! retry later')

#fseek ftell cv2 documentation - read about it 
#need to increase the size of the images...
#need to make it into a function