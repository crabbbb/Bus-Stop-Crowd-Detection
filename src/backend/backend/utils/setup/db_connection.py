from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from backend.utils import FileManage
import os
import errno
from django.conf import settings 
from typing import Tuple, Dict

class MongoDB :
    __client = None
    __uri = None
    __default_db = None

    def __init__(self):
        pass

    '''
    do URL Encoding to prevent special character conflict with reserved syntax 
    param : 
        password : user password
    return : 
        encoded password 
    '''
    @classmethod
    def __urlEncode(cls, password: str) -> str : 
        from urllib.parse import quote
        return quote(password)
    
    '''
    prepare database configuration by reading configuration detail from env and yaml
    return :
        database configuaration in dictionary, None if file not exist
    '''
    @classmethod
    def __loadDBConfig(cls) -> dict :

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
            "uPass": cls.__urlEncode(envConfig("DB_PASSWORD")),
            "host": yaml_config["database"]["host"],
            "options": yaml_config["database"]["options"]
        }

        return dbConfig
    
    @classmethod
    def __getDefaultDB(cls) : 
        cls.__default_db = FileManage.readYAML(os.path.join(settings.BASE_DIR, "backend/config/db_config.yaml"))["database"]["databaseName"]
    
    @classmethod
    def setDefaultDB(cls, dbName: str) -> bool : 
        cls.__default_db = dbName
        return True
    
    @classmethod
    def getDBName(cls) -> str : 
        return cls.__default_db
    
    @classmethod
    def getDBInfo(cls) -> Tuple[Dict[str, str], str] : 
        try : 
            dbConfig = cls.__loadDBConfig()
        except FileNotFoundError as e :
            # raise FileNotFoundError(e)
            print(f"Configuration file for storing the database information not found > {e}")
            return None, None

        uri = f"mongodb+srv://{dbConfig['uName']}:{dbConfig['uPass']}@{dbConfig['host']}/{dbConfig['options']}"

        # no preset, use default 
        if cls.getDBName() == None : 
            # get default
            cls.__getDefaultDB()

        return uri, cls.getDBName()

    '''
    return : 
        bool - true if connect success, false when file not exist 
    error : 
        connection error if the configuration inside the file is incorrect 
    '''
    @classmethod
    def activate_client(cls) -> bool : 
        
        try :
            if cls.__client is None : 
                # client is not active 
                if cls.__uri is None : 
                    # uri not ready
                    cls.__uri, cls.__default_db = cls.getDBInfo()

                    if cls.__uri is None : 
                        # if still None after getDBInfo means file not exist 
                        return False

                # activate client
                cls.__client = MongoClient(cls.__uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
                # send ping command to mongodb server to ensure the connection is active and reachable 
                response = cls.__client.admin.command('ping')

                # print response 
                print(f"MongoDB Connection Successful : {response}")

            return True
        except ConnectionError as e : 
            # have file but configuration wrong or internet conection problem
            raise ConnectionFailure(f"Error No : {errno.ENOTCONN}. MongoDB Connection Unsuccessful > {e}")
        
    @classmethod
    def isActive(cls) : 
        return True if cls.__client is not None else False
    
    @classmethod
    def terminateConnection(cls) : 
        if cls.__client : 
            cls.__client.close()
            cls.__client = None
    
    # check connection status 
    @classmethod
    def isHealthy(cls) :
        try:
            if not cls.isActive() :
                # not connected 
                return False
            
            response = cls.__client.admin.command('ping')
            print(f"MongoDB still connected : {response}")
            return True
        except Exception:
            return False
    
    @classmethod
    def reconnect(cls) :
        try : 
            cls.terminateConnection()
            if not cls.activate_client() : 
                # configuration file problem 
                return False
        except ConnectionError as e : 
            raise ConnectionError(e)


    @classmethod
    def getDB(cls, dbName = None) :
        try :
            if dbName is not None : 
                cls.setDefaultDB(dbName=dbName)

            if cls.__client == None :
                # class not active 
                if not cls.activate_client() : 
                    # activate unsuccess with no error 
                    # file not found = db info not inside the file 
                    return None 

            # client is activate / success activate 
            # return db 
            return cls.__client[cls.getDBName()]
        except ConnectionError as e : 
            raise ConnectionError(e)


# singleton instance 
mongo = MongoDB()