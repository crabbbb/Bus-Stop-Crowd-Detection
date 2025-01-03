from pymongo.database import Database
from backend.utils import FileManage
import numpy as np
from .db_connection import mongo
import os
from django.conf import settings 

class Database :
    __db = None 

    def __init__(self, dbName = None):
        # getDatabase will bring help on create database 
        try :
            self.__db = mongo.getDB(dbName=dbName) 
        except ConnectionError as e : 
            self.__db = None

    @classmethod
    def isConnected(self) :
        return True if self.__db is not None else False
    
    '''
    return list of connection names that store inside the db_config.yaml file  
    return : 
        
    ''' 
    @staticmethod
    def __getPresetCollectionsName() : 
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
        if collection in self.__db.list_collection_names() : 
            return True 
        return False 

    def isSameCollections(self, collections: str = None) -> bool: 
        currentCollections = self.__db.list_collection_names()

        if not collections :
            # get the collections list from yaml file
            collections = Database.__getPresetCollectionsName()
        
        if set(collections).issubset(set(currentCollections)) and len(currentCollections) == len(currentCollections) : 
            return True
        
        return False

    def numOfCollections(self) -> np.int64:
        return len(self.__db.list_collection_names())

    def dropAllCollections(self) : 
        for c in self.__db.list_collection_names() : 
            collection = self.__db[c]
            collection.drop()
            print(f"Drop Collection - {c} collections drop sucess")
        return True if len(self.__db.list_collection_names()) == 0 else False

    def createCollection(self, name: str, data: list = None) -> bool: 
        try : 
            # create 
            self.__db.create_collection(name=name)
            if data : 
                collection = self.__db[name]
                collection.insert_many(data)
            return True
        except Exception as e:
            print(e)
            return False
    
    # reset the database by using the collections list pass  in
    def resetDB(self, collections: str = None) -> np.int64: 
        if not collections : 
            # get the collections from yaml file 
            collections = Database.__getPresetCollectionsName()

        # if collection exist will drop the collections 
        if self.__db is not None :
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
    
    def getCollection(self, collectionName : str) :
        # check exist 
        if not self.isCollectionExist(collection=collectionName) :
            return None 
        
        # collection exits in this database 
        return self.__db[collectionName]


