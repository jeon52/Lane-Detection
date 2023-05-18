Notes:
lane_input_test.py
lane_detection.py       - these two files were not written by me. only changed a few lines of code

requirements.txt
    - Changed versions of the libraries to download 1 version
    - Required a long time of trial and error since some versions of the libraries require other version of libraries to be downloaded together
    - only takes about 10 mins to download now (originally about 10 hrs)

lane_input_test.py
    - new line of code: matplotlib.use('TkAgg')
    - required code for running the dataset

lane_detection.py
    - Changed the directory of the dataset
    - input_path: str = '/Users/bradjeon/dataset/Dataset/bdd100k-val*'
    - bdd100k-val* is enough for the name - do not need to write the whole name

*From here: The code from here starts to builds up! I will be implementing what I have learned in the previous scripts. 

jsonfiledataextraction.py
    - First functional script written by me 
    - this script allows me to extract necessary information from the json file
    - extraction will usually be done in the form of a list

overlayimage.py
    - uses basic linear algebra (matrix addition) to overlay 2 different images of same resolution into original image
    - basic use of numpy (making blank image file) and opencv to open images 
    - rank : bounding boxes > lanes > drivable area > original image
    - bounding boxes are not done yet

parsingimages.py
    - implementation of os to parse through different directories 
    - images with the same name (but different ext) will be found
    - this script allows sequential overlay of the dataset

pingingserver.py   
    - pings the bdd100k server to check if the server is up or down
    - using names extracted from the json file, find the necessary video 
    - play the video with cv2 - this is different from opening up an image file

specificframe.py
    - This script involves me doing some testing with waitkey() function 
    - This script will allow me to get to the specific frame of the video without having to play the whole video 
    - will get 5 frames before and after relative to the 10 seconds mark of the videos 

specificframeallatonce.py
    - this script shows all the frames (5 - 15 sec frames, so 11 in total) in one figure
    - this involves the use of matplotlib library 
    - more work is needed to change the size of the subplots (images) in the figure

create_bdd100k-tf_record.py
    - This is a script that is written by Pume
    - I added the function of my own(specificframe.py). Some changes were made!
    - The function returns 13 frames per videos. Therefore, if I process 1000 videos, it will return an array of 13000 frames (elements)
    - The function takes processing (on my laptop might be faster or slower depending on the cpu)
        10 videos - 2 mins 38 seconds
        35 videos - 10 mins 38 seconds (error on 21st video - timeout error?)
        50 videos - 18 mins 13 seconds 
        77 videos - 37 mins 40 seconds
        93 videos - 46 mins 50 seconds
        100 videos - 52 mins
        123 videos - 1 hour 10 seconds
        155 videos - 1 hour 19 mins 25 seconds
        175 videos - 1 hour 30 mins 10 seconds 
        200 videos - 1 hour 46 mins 55 seconds
        300 videos - 2 hours 41 mins
        400 videos - 3 hours 34 mins
        500 videos - 4 hours 27 mins

Commands: 51 mins 46 seconds 
    - command for running the dataset: python -m ipa.dataloaders.lane_input_test 
        - must activate virtual environment: conda activate ipa
        - must be inside the Lane_S21 directory
    - code for running the requirements.txt: pip install -r requirements.txt
        - must be in the ipa folder
        - must activate virtual environment: conda activate ipa
    - linux commands: (Examples)
        1. conda list
            lists all the versions of libraries downloaded in the virtual environment. 
        2. pip install numpy==1.19.5
            specifies version of numpy (or other libraries)
            >= is also available but takes much more time 
        3. pip uninstall numpy 
        4. conda install -y -c conda-forge numpy==1.19.5
            try this if there are any errors 
