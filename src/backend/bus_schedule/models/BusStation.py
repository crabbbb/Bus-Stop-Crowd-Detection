from .supermodel import SuperModel

class BusStation(SuperModel) :
    __collection = "BusStation"
    __idHead = "BS"
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead, "StationName")

    def createOne(self, data : dict):
        try : 
            collection = self.__getCollection()

            # check collection exist 
            if collection is None : 
                return None

            # have id and data 
            result = collection.insert_one(data)

            return result
        except ConnectionError as e :
            raise ConnectionError(e)
        except ValueError as e :
            raise ValueError(e)