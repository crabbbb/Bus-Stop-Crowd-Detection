from .db_database import Database
from django.db import connections
from django.db.utils import OperationalError
from . import * 

def setup() -> str : 
    dbName = getDefaultDB() 
    db = None
    try : 
        # check djongo connect success or not 
        conn = connections['default']

        # build connection 
        if conn.connection is None : 
            conn.cursor()  
            print("Django successfully connect to MongoDB")

        # best case, database exist and collections exist 
        db = Database(dbName=dbName)

        # check len and the collections name is same with current collections inside the mongodb 
        if db.isSameCollections() :
            print("Database setting correct, connect to existing database")
            return dbName
        
        # only create database and not same collections will reach here 
        db.resetDB()
        print("Database reset successfully")
        return dbName 
    except OperationalError as e : 
        print(f"Djongo unable to connect MongoDB : {e}")
        return None 
    except Exception as e :
        print(e)
        return None

# for mannual command use 
def resetCollections() : 
    dbName = getDefaultDB() 
    db = None
    try : 
        # check djongo connect success or not 
        conn = connections['default']

        # build connection 
        if conn.connection is None : 
            conn.cursor()  
            print("Django successfully connect to MongoDB")

        # direct reset the collections 
        db = Database(dbName=dbName)

        db.resetDB()

        print("Database reset successfully ")
    except OperationalError as e : 
        print(f"Djongo unable to connect MongoDB : {e}")
        return None 
    except Exception as e :
        print(e)
        return None