from .db_database import Database
from django.db import connections
from django.db.utils import OperationalError
from ..setup import mongo 

def setup() -> bool : 
    try : 
        # using getdb direct build connection 
        db = mongo.getDB()

        # check None 
        if db is None : 
            # file not found 
            print("Database configuration file not exist")
        
        # db exist means everythings is ready 
        # reset start 
        db = Database()

        # check the collection name is same with current collections inside the mongodb
        if db.isSameCollections() : 
            print("Database setting correct, connect to existing database")
            return True
        
        # only create database and not same collections will reach here 
        db.resetDB()
        print("Database reset successfully")
        return True
    except ConnectionError as e : 
        print(f"Setup unsuccessful due to not able to connect with MongoDB > {e}")
        return False
    except Exception as e : 
        print(f"Setup unsuccessful due to unexpected error happen > {e}")
        return False

# for mannual command use 
def resetCollections() -> bool : 
    try : 
        # using getdb direct build connection 
        db = mongo.getDB()

        # check None 
        if db is None : 
            # file not found 
            print("Database configuration file not exist")
        
        # db exist means everythings is ready 
        # reset start 
        db = Database()
        
        db.resetDB()
        print("Database reset successfully")
        return True
    except ConnectionError as e : 
        print(f"Reset unsuccessful due to not able to connect with MongoDB > {e}")
        return False
    except Exception as e : 
        print(f"Reset unsuccessful due to unexpected error happen > {e}")
        return False