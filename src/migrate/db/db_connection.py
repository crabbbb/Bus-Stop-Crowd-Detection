from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from utils import FileManage
import os
import errno

_HOME = os.path.join(os.path.dirname(__file__), "../")

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
    yamlFile = os.path.join(_HOME, "config/db_config.yaml")

    if not os.path.exists(yamlFile) : 
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yamlFile)
    
    # read .env file locally 
    from dotenv import load_dotenv
    # load env variable from .env file 
    load_dotenv(dotenv_path=os.path.join(_HOME, "config/.env"))

    # read yaml file 
    config = FileManage.readYAML(yamlFile)

    # combine env and yaml become a complete config
    # encode the url to prevent conflict special symbol
    dbConfig = {
        "uName": os.getenv("DB_USER"),
        "uPass": _urlEncode(os.getenv("DB_PASSWORD")),
        "host": config["database"]["host"],
        "options": config["database"]["options"]
    }

    return dbConfig

'''
build connection with mongodb 
error : 
    ConnectionFailure - unable to connect mongodb 
return : 
    None if error occurs else will return MongoClient
'''
def _connectToMongoDB() :
    try : 
        dbConfig = _loadDBConfig()
    except FileNotFoundError as e :
        raise FileNotFoundError(e)

    uri = f"mongodb+srv://{dbConfig['uName']}:{dbConfig['uPass']}@{dbConfig['host']}/{dbConfig['options']}"

    try : 
        # connect with mongodb 
        client = MongoClient(uri, server_api=ServerApi('1'))

        # send ping command to mongodb server to ensure the connection is active and reachable 
        response = client.admin.command('ping')
        print(f"MongoDB Connection Successful > {response}")
        return client 
    except ConnectionFailure as e : 
        raise ConnectionFailure(errno.ENOTCONN, f"MongoDB Connection Unsuccessful > {e}")

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
            print(e)
            terminateConnection()
        except FileNotFoundError as e : 
            print(e)
            terminateConnection()

def terminateConnection() : 
    global _client
    
    if _client : 
        _client.close()
        _client = None

def isConnected() -> bool : 
    return True if _client else False

@property
def client() :
    return _client

# database 

'''
to check the database exist or not 
return : 
    True when is exist else False 
''' 
def isDBExist(dbName: str) -> bool :
    if dbName in _client.list_database_names() : 
        return True
    return False 

def getDatabase(dbName: str) :
    # if database exist will return database else will create a new one 
    return _client[dbName]

def getDefaultDB() -> str : 
    return FileManage.readYAML(os.path.join(_HOME, "config/db_config.yaml"))["database"]["databaseName"]