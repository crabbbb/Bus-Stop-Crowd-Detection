from pymongo import MongoClient
from pymongo.database import Database
from backend.utils import FileManage
import numpy as np
from .db_connection import getDatabase
import os
from django.conf import settings 

class Database :

    def __init__(self, dbName):
        # getDatabase will bring help on create database 
        self._db = getDatabase(dbName=dbName) 
    
    '''
    return list of connection names that store inside the db_config.yaml file  
    return : 
        
    ''' 
    def _getPresetCollectionsName() : 
        yamlFile = os.path.join(settings.BASE_DIR, "backend/config/db_config.yaml")
        # read yaml file 
        config = FileManage.readYAML(yamlFile)
        
        return config['collections']

    '''
    to check the collections exist or not 
    return : 
        True when is exist else False 
    ''' 
    def isCollectionExist(self, collection: str) -> bool: 
        if collection in self._db.list_collection_names() : 
            return True 
        return False 

    def isSameCollections(self, collections: str = None) -> bool: 
        currentCollections = self._db.list_collection_names()

        if not collections :
            # get the collections list from yaml file
            collections = Database._getPresetCollectionsName()
        
        if set(collections).issubset(set(currentCollections)) and len(currentCollections) == len(currentCollections) : 
            return True
        
        return False

    def numOfCollections(self) -> np.int64:
        return len(self._db.list_collection_names())

    def dropAllCollections(self) : 
        for c in self._db.list_collection_names() : 
            collection = self._db[c]
            collection.drop()
            print(f"Drop Collection - {c} collections drop sucess")
        return True if len(self._db.list_collection_names()) == 0 else False

    def createCollection(self, name: str, data: list = None) -> bool: 
        try : 
            # create 
            self._db.create_collection(name=name)
            if data : 
                collection = self._db[name]
                collection.insert_many(data)
            return True
        except Exception as e:
            print(e)
            return False
    
    # reset the database by using the collections list pass  in
    def resetDB(self, collections: str = None) -> np.int64: 
        if not collections : 
            # get the collections from yaml file 
            collections = Database._getPresetCollectionsName()

        # if collection exist will drop the collections 
        if self._db :
            if self.numOfCollections() > 0: 
                # drop all collections and create again
                self.dropAllCollections()
        
        # NOTE : Ensure each json file is same with the collections name
        # loop and create collections and assign data 
        unsuccessNo = 0
        filePath = os.path.join(settings.BASE_DIR, "backend/utils/setup/db_init/")
        for c in collections : 
            data = FileManage.readJson(os.path.join(filePath, f"{c}.json"))
            if not Database.createCollection(self, name=c, data=data) : 
                print(f"Error : Collection {c} data unable to be added")
                unsuccessNo += 1
            print(f"Create Collection - {c} data added to MongoDB successfully")
        return unsuccessNo

