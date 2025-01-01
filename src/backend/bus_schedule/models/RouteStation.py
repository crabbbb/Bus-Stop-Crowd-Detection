from .supermodel import SuperModel
from .Route import Route
from .BusStation import BusStation

class RouteStation(SuperModel) :
    __collection = "RouteStation"
    __idHead = ""
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead)
        self.__idName = "RouteId"

    # override the getByID function 
    def getWithID(self, idData : str) : 
        try : 
            collection = super()._getCollection()

            # check collection exist 
            if collection is None : 
                return None 
            
            # get data with using id 
            result = list(collection.find({self.__idName : idData}))

            if result : 
                # have data 
                return result
            
            return result
        except ConnectionError as e : 
            raise ConnectionError(e)
        
    def createOne(self, data : dict) :
        try : 
            collection = self._getCollection()

            # check collection exist 
            if collection is None : 
                return None
            
            # check station exist, and route exist 
            route = Route()
            r = route.getWithID(data["RouteId"])

            if not r : 
                # raise error 
                raise ValueError("Invalid Route Id")
            
            station = BusStation()
            s = station.getWithID(data["StationName"])
            if not s : 
                raise ValueError("Invalid Station Name")

            # have id and data 
            result = collection.insert_one(data)

            return result
        except ConnectionError as e :
            raise ConnectionError(e)
        except ValueError as e :
            raise ValueError(e)
    
    def deleteOne(self, routeId, stationName):
        try : 
            collection = self._getCollection()

            # check collection exist
            if collection is None : 
                return None

            # return None if data doesnot exist 
            result = collection.find_one_and_delete({"RouteId" : routeId, "StationName" : stationName})

            return result 
        except ConnectionError as e :
            raise ConnectionError(e)