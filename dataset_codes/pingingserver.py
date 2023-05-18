import os
import numpy as np
import cv2
import json

hostip = "128.32.162.150" #bdd100k Server IP address
hostname = "http://dl.yf.io/bdd100k/videos/" #address of where all the videos are located #change this 
#https://www.yf.io/#services or http://dl.yf.io/bdd100k/videos/
ext = ".mov" #extension for videos in the website
#response = os.system("ping -c 1" + hostip) #send ping to the server
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

      #load video from the website
      video = cv2.VideoCapture(hostname + videowithext)
      if video.isOpened() is None: #if the video is not loaded
        print (video, "video cannot be loaded")

      while(video.isOpened()):
        # Capture frame-by-frame
        ret, frame = video.read()
        if ret == True:
          cv2.imshow('frame',frame) # Display video
          if cv2.waitKey(1) & 0xFF == ord("q"): #delay time is ms, in this case 1ms
            break
        else:
          break
          #cv2.waitKey(0) #press something to go to the next frame 

      # When everything done, release the capture
      cv2.destroyAllWindows()
      video.release()
      print ("next video")

else: #response not back 
  print (hostip, 'the website is down! retry later')

#find frames per second using cv.2 
#scrubbing previous and after 5 seconds 
#after 10 second mark 
#fseek ftell cv2 documentation - read about it 