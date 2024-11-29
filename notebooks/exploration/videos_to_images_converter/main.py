import os
import cv2 
from file import FileManage

videoNameList = ["VideoConvertImage3"]
sourcePath = "C:/Users/LENOVO/OneDrive/Documents/GitHub/Crowd-Detection/Source/CCTV/"
brightnessLevel = 50

for v in videoNameList : 
    # get the video path 
    video = os.path.join(sourcePath, f"{v}.mp4")
    print(video)
    if not FileManage.isExist(video) :
        # yes, no exist
        print(f"Error ! video doesnot exist - {video}")
        break
    
    # create folder 
    folder = os.path.join(sourcePath, v)
    if not FileManage.isExist(folder) : 
        # not exist create a new 
        FileManage.createFolder(folder)
    
    frameNo = 0

    # capture the video
    cap = cv2.VideoCapture(video)
    while cap.isOpened() : 
        # read success 
        ret, frame = cap.read()
        if not ret : 
            # false, doesnot read properly 
            exit()
            
        # increase the brightness of picture 
        brightImage = cv2.add(frame, brightnessLevel)

        # image name 
        imName = os.path.join(folder, f"frame_{frameNo}.jpg")
        frameNo += 1

        if not FileManage.isExist(imName) : 
            FileManage.savePic(brightImage, filepath=imName)
    
    # display end 
    print(f"Total Number of frame for folder {v} is {frame + 1}")