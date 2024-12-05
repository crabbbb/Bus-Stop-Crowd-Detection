from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from backend.utils import FileManage
import os
import errno
from django.conf import settings 
from typing import Tuple, Dict
from django.db import connection


'''
do URL Encoding to prevent special character conflict with reserved syntax 
param : 
    password : user password
return : 
    encoded password 
'''
def _urlEncode(password: str) -> str : 
    from urllib.parse import quote
    return quote(password)

'''
prepare database configuration by reading configuration detail from env and yaml
return :
    database configuaration in dictionary, None if file not exist
'''
def _loadDBConfig() -> dict :

    # check db_config.yaml exist 
    yamlFile = os.path.join(settings.BASE_DIR, "backend/config/db_config.yaml")
    envFile = os.path.join(settings.BASE_DIR, "backend/config/.env")

    if not os.path.exists(yamlFile) or not os.path.exists(envFile): 
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yamlFile)
    
    # read .env file locally 
    from decouple import Config, RepositoryEnv

    # load env variable from .env file 
    envConfig = Config(RepositoryEnv(envFile))

    # read yaml file 
    yaml_config = FileManage.readYAML(yamlFile)

    # combine env and yaml become a complete config
    # encode the url to prevent conflict special symbol
    dbConfig = {
        "uName": envConfig("DB_USER"),
        "uPass": _urlEncode(envConfig("DB_PASSWORD")),
        "host": yaml_config["database"]["host"],
        "options": yaml_config["database"]["options"]
    }

    return dbConfig

def getDBInfo() -> Tuple[Dict[str, str], str] : 
    try : 
        dbConfig = _loadDBConfig()
    except FileNotFoundError as e :
        # raise FileNotFoundError(e)
        print(f"Configuration file for storing the database information not found > {e}")

    uri = f"mongodb+srv://{dbConfig['uName']}:{dbConfig['uPass']}@{dbConfig['host']}/{dbConfig['options']}"

    return uri, getDefaultDB()

'''
build connection with mongodb 
error : 
    ConnectionFailure - unable to connect mongodb 
return : 
    None if error occurs else will return MongoClient
'''
def _connectToMongoDB() :

    uri, _ = getDBInfo()

    try : 
        # connect with mongodb 
        client = MongoClient(uri, server_api=ServerApi('1'))

        # send ping command to mongodb server to ensure the connection is active and reachable 
        response = client.admin.command('ping')
        print(f"MongoDB Connection Successful : {response}")
        return client 
    except ConnectionFailure as e : 
        raise ConnectionFailure(f"Error No : {errno.ENOTCONN}. MongoDB Connection Unsuccessful : {e}")

# singleton 
_client = None

# call connection
def buildConnection() : 
    global _client

    if _client is None : 
        # initialize the client 
        from pymongo.errors import ConnectionFailure
        try : 
            _client = _connectToMongoDB()
        except ConnectionFailure as e : 
            print(f"Connection Failure : {e}")
            terminateConnection()
        except FileNotFoundError as e : 
            print(f"File Not Found Failure : {e}")
            terminateConnection()

def terminateConnection() : 
    global _client
    
    if _client : 
        _client.close()
        _client = None

def _getDjongoClient() -> MongoClient: 
    from django.db import connection

    try:
        # get the djongo client for pymongo use 
        client = connection.cursor().client
        print("Successfully access Pymongo MongoClient")
        return client
    except Exception as e:
        print(f"Error accessing MongoClient : {e}")
        return None

# database 

def getDatabase(dbName: str) :
    # if database exist will return database else will create a new one 
    client = _getDjongoClient()
    return client[dbName]

def getDefaultDB() -> str : 
    return FileManage.readYAML(os.path.join(settings.BASE_DIR, "backend/config/db_config.yaml"))["database"]["databaseName"]