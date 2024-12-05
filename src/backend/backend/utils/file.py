import os
import json 
import yaml

class FileManage :

    def isExist(filePath: str) -> bool : 
        if os.path.exists(filePath) : 
            return True 
        return False 
    
    def readYAML(filePath: str) -> dict : 
        if FileManage.isExist(filePath) : 
            with open(filePath, "r") as f : 
                return yaml.safe_load(f)

    def readJson(filePath: str) -> dict : 
        if FileManage.isExist(filePath) : 
            with open(filePath, "r") as f : 
                return json.load(f)