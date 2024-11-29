from pymongo import MongoClient
from pymongo.database import Database
import yaml
import os
import errno

'''
to check the database exist or not 
return : 
    True when is exist else False 
''' 
def isDBExist(dbName: str, client: MongoClient) -> bool :
    if dbName in client.list_database_names() : 
        return True
    return False 

'''
to check the collections exist or not 
return : 
    True when is exist else False 
''' 
def isCollectionExist(collection: str, db: Database) : 
    if collection in db.list_collection_names() : 
        return True 
    return False 

def isSameCollections(collections1: str, collections2: str) : 
    if set(collections1).issubset(set(collections2)) and len(collections2) == len(collections2) : 
        return True
    return False

'''
return list of connection names that store inside the db_config.yaml file  
return : 
    
''' 
def getCollections(yamlFile) -> str : 
    # read yaml file 
    with open(yamlFile, "r") as f : 
        config = yaml.safe_load(f)
    
    return config["databaseCollection"]

def dropAllCollections(db: Database) : 
    for c in db.list_collection_names() : 
        collection = db[c]
        collection.drop()
    return True if len(db.list_collection_names()) == 0 else False

'''
create collection based on the collection list pass in 
param : 
    db : the database that have exist in the database server connect , must in pymongo.database.Database
    collections : a list of connection names 
'''
def createCollections(db: Database, collections: str) : 
    # check all collections exist
    if not isSameCollections(db.list_collection_names(), collections) : 
        # drop all collections and create again
        dropAllCollections(db)

        