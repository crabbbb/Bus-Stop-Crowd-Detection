from backend.utils import mongo
import numpy as np

# if all the data dont have found will only return empty list []
class SuperModel :

    __collectionName = None 
    __idHead = None
    __idName = None

    def __init__(self, collectionName : str, idHead : str) :
        self.__collectionName = collectionName
        self.__idHead = idHead
        self.__idName = f"{self.__collectionName}Id"

    '''
    return collection instance 
    error - Connection error 
    '''
    def __getCollection(self) : 
        try :
            if not mongo.isHealthy() :
                # either no connect or connection down 
                if not mongo.reconnect() : 
                    # unable to connect due to file problem 
                    return None
            
            # have connection, get collection 
            db = mongo.getDB()
            return db[self.__collectionName]
        except ConnectionError as e : 
            # for view to handle 
            raise ConnectionError(e) 

    def getAll(self) :
        try : 
            collection = self.__getCollection()

            # check collection exist 
            if collection is None : 
                return None
            
            # have collection get data 
            # put list to prevent lazily fetches data
            return list(collection.find())
        except ConnectionError as e : 
            raise ConnectionError(e)
    
    # bridge table request overwrite this 
    def getWithID(self, idData : str) : 

        try : 
            collection = self.__getCollection()

            # check collection exist 
            if collection is None : 
                return None 
            
            # get data with using id 
            return list(collection.find({self.__idName : idData}))
        except ConnectionError as e : 
            raise ConnectionError(e)
        
    def getByfilter(self, filterCondition : dict, options : dict = None) : 
        try : 
            collection = self.__getCollection()

            # check collection exist
            if collection is None : 
                return None
            
            # check option have or not 
            if not options : 
                # pass in filter 
                return list(collection.find(filterCondition))
            else : 
                # pass in with options 
                return list(collection.find(filterCondition, options))
        except ConnectionError as e :
            raise ConnectionError(e)

    def getAllSimilar(self, columnName : str, value : str, options : dict = None) :
        try : 
            collection = self.__getCollection()

            # check collection exist
            if collection is None : 
                return None
            
            if options is None : 
                return collection.find({columnName : {"$regex" : value}})
            
            # with option 
            return collection.find({columnName : {"$regex" : value}}, options)
        except ConnectionError as e :
            raise ConnectionError(e)

    def updateOne(self, updatedData : dict) :

        try : 
            collection = self.__getCollection()

            # check collection exist
            if collection is None : 
                return None
            
            # remove busid 
            idData = updatedData.pop(self.__idName, None)

            if not idData or idData.strip() == "" : 
                # id not exist 
                return None
            
            # filter query
            filterQuery = {self.__idName : idData}
            
            # (filter, update data, option to return updated data)
            result = collection.find_one_and_update(
                filterQuery,
                {"$set": updatedData},
                return_document=True
            )
            
            # result.matched_count == result.modified_count 
            return result
            
        except ConnectionError as e : 
            raise ConnectionError(e)
    
    def deleteOne(self, idData : str) : 

        try : 
            collection = self.__getCollection()

            # check collection exist
            if collection is None : 
                return None

            # return None if data doesnot exist 
            result = collection.find_one_and_delete({self.__idName : idData})

            return result 
        except ConnectionError as e :
            raise ConnectionError(e)
        
    def sortById(self, order : np.int64) :

        try : 
            collection = self.__getCollection()

            # check collection exist
            if collection is None : 
                return None
            
            # 1 = ascending order 
            sortedData = list(collection.find().sort(self.__idName, order))

            print(sortedData)

            return sortedData

        except ConnectionError as e : 
            raise ConnectionError(e)
    
    def getLatestId(self) :

        try :
            sortedData = self.sortById(order=-1)

            # check None or empty
            # either configuration file problem or database dont have data 
            if sortedData is None : 
                # file problem 
                return None
                
            if not sortedData : 
                # no data 
                # is database dont have data 
                return f"{self.__idHead}001"
            
            # have data 
            latest = sortedData[0][self.__idName]

            # the idHead not match with what database have 
            if self.__idHead not in latest:
                raise ValueError(f"Invalid ID format: {latest}")

            numericPart = int(latest.split(self.__idHead)[1]) + 1

            return f"{self.__idHead}{numericPart:03d}"
        except ConnectionError as e :
            raise ConnectionError(e)
        except ValueError as e :
            raise ValueError(e)

    def createOne(self, data : dict) :
        try : 
            collection = self.__getCollection()

            # check collection exist 
            if collection is None : 
                return None
            
            # get the latest id 
            lastestID = self.getLatestId()
            
            data[self.__idName] = lastestID

            # have id and data 
            result = collection.insert_one(data)

            return result
        except ConnectionError as e :
            raise ConnectionError(e)
        except ValueError as e :
            raise ValueError(e)