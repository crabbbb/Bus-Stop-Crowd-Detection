from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from pymongo.database import Database
import yaml
import os
import errno

__HOME = os.path.join(os.path.dirname(__file__), "../")

'''
do URL Encoding to prevent special character conflict with reserved syntax 
param : 
    password : user password
return : 
    encoded password 
'''
def urlEncode(password: str) -> str : 
    from urllib.parse import quote
    return quote(password)

'''
prepare database configuration by reading configuration detail from env and yaml
return :
    database configuaration in dictionary, None if file not exist
'''
def __loadDBConfig() -> dict :
    # check db_config.yaml exist 
    yamlFile = os.path.join(__HOME, "config/db_config.yaml")

    if not os.path.exists(yamlFile) : 
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yamlFile)
    
    # read .env file locally 
    from dotenv import load_dotenv
    # load env variable from .env file 
    load_dotenv()

    # read yaml file 
    with open(yamlFile, "r") as f : 
        config = yaml.safe_load(f)

    # combine env and yaml become a complete config
    dbConfig = {
        "uName": os.getenv("DB_USER"),
        "uPass": os.getenv("DB_PASSWORD"),
        "host": config["database"]["host"],
        "dbName": config["database"]["databaseName"],
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
def connectToMongoDB() :
    try : 
        dbConfig = __loadDBConfig()
    except FileNotFoundError as e :
        raise FileNotFoundError(e)

    uri = f"mongodb+srv://{dbConfig['uName']}:{dbConfig['uPass']}@{dbConfig['host']}/{dbConfig['dbName']}{dbConfig['options']}"

    try : 
        # connect with mongodb 
        client = MongoClient(uri, server_api=ServerApi('1'))

        # send ping command to mongodb server to ensure the connection is active and reachable 
        response = client.admin.command('ping')
        print(f"MongoDB Connection Successful > {response}")

        return client 
    except ConnectionFailure as e : 
        raise ConnectionFailure(errno.ENOTCONN, f"MongoDB Connection Unsuccessful > {e}")
