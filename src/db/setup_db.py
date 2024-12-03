from .db_database import Database
from . import * 

def setup() -> bool: 
    dbName = getDefaultDB()
    db = None
    try : 
        # connect mongodb
        buildConnection()
        if isConnected() :
            # best case, database exist and collections exist 
            db = Database(dbName=dbName)
            if db.isSameCollections() :
                print("Database setting correct, connect to existing database")
                return True
            
            # only create database and not same collections will reach here 
            db.resetDB()
            print("Database reset successfully")
            return True 
        else : 
            # unable to connect client 
            print("Error : Unable to connect MongoDB")
            return False
    except Exception as e :
        print(e)
        return False
    finally : 
        # end the connection, for setup 
        terminateConnection()