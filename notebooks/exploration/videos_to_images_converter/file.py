import os 
import cv2

class FileManage :

    def isExist(path) : 

        if os.path.exists(path) : 
            return True 
        else : 
            return False 

    def createFolder(filepath) : 

        if FileManage.isExist(filepath) : 
            # if folder exist 
            print(f"Folder exist - {filepath}")
            return False

        # not exist - create 
        try : 
            os.mkdir(filepath)
            # print(f"Folder create successfully. {fpath}")
            return True
        except FileExistsError : 
            print(f"Folder create unsuccessful. {filepath}")
    
    def savePic(image, filepath) :
        
        if FileManage.isExist(filepath) : 
            print(f"Image exists - {filepath}")
            return False
        
        # not exist - create 
        cv2.imwrite(filepath, image)
        return True