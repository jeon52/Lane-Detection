import os
import numpy as np
import cv2
import json

#get a example image from the dataset, get its height, width, and channel 
example = cv2.imread('/Users/bradjeon/dataset/Dataset_Updates/bdd100k-4/images/100k/train/0a0a0b1a-7c39d841.jpg')
(H1, W1, C1) = example.shape

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

      # get information regarding the video
      #framecount = video.get(cv2.CAP_PROP_FRAME_COUNT) #total number of frames 
      #print("number of frames", framecount)
      fps = video.get(cv2.CAP_PROP_FPS) #gets frames per second of the video
      print("fps", fps)
      #print("1/fps", 1/fps) #this is a decimal value not a integer
      #print("1/fps with integer cast", int(1/fps)) #this will not work... as it will convert to 0
      #duration = framecount / fps #get the duration of each videos
      #print("duration of video in seconds", duration)

      startingpoint = round(fps * 5) #checked with the original dataset!!! matches!!!
      #do not do int(fps * 10) or int(fps * 10) - 1 - this will only round down!!!
      i = 0 #initialization

      for i in range (12):
        if i == 11: #make sure i does not go over 10
          cv2.destroyAllWindows()
          video.release()
          print ("next video")
          break
        sequentialpoint = startingpoint + round(fps * i) #starts from default 0 therefore, the video starts at 5 seconds
        print("SECONDS", i + 5)
        video.set(cv2.CAP_PROP_POS_FRAMES, sequentialpoint)
        ret, frame = video.read()
        if ret == True:
          cv2.imshow('frame', frame) # Display video
          if cv2.waitKey(0) & 0xFF == ord("q"): #delay time is ms, in this case 1ms
            break
        else:
          break

      # When everything done, release the capture
      #cv2.destroyAllWindows()
      #video.release()
      #print ("next video")

else: #response not back 
  print (hostip, 'the website is down! retry later')

#fseek ftell cv2 documentation - read about it 
#save 5 frames after and before the 10th second.
#frame at the 5th second and 15th second.
#for the function return - N number of frames 