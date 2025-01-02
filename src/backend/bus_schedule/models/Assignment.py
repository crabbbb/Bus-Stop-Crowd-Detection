from .supermodel import SuperModel

class Assignment(SuperModel) :
    __collection = "Assignment"
    __idHead = "A"
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead)
    
    # @staticmethod
    # def getNextBus(stationName) : 
    #     # get current date and time
    #     now = datetime.now()

    #     currentTime = now.strftime("%H:%M:%S")

    #     # Get the day of the week as an integer (0=Monday, 6=Sunday)
    #     now = datetime.now()
    #     dayOfWeek = now.weekday() # mine is 1 = mon
    #     query = {
    #         "Time": {"$gte": currentTime},
    #         "DayOfWeek" : {"$eq": dayOfWeek}
    #     }

    #     try : 
    #         collection = super()._getCollection()

    #         # check collection exist 
    #         if collection is None : 
    #             return None 
            
    #         # get data with using id 
    #         nearestTimeRecord = collection.find(query, sort=[("Time", 1)])
    #         print(f"nearest Time Record > {nearestTimeRecord}")

    #         if nearestTimeRecord : 
    #             # have data 
    #             stationId = collection.find({"StationName" : {"$eq": stationName}})
    #             print(f"StationId > {stationId}")
    #             routeStation = RouteStation()
                
    #             filter = {
    #                 "StationId": {"$eq": stationId},
    #                 "RouteOrder": {"$eq": 1}
    #             }

    #             rsResult = routeStation.getByfilter(filter)
    #             print(f"rsResult > {rsResult}")
    #             if rsResult : 
    #                 for nearest in nearestTimeRecord : 
    #                     if nearest["RouteId"] in rsResult : 
    #                         bus = Bus()
    #                         busCapacity = bus.getWithID(nearest["BusId"])
    #                         return nearest, busCapacity
            
    #         return None
    #     except ConnectionError as e : 
    #         raise ConnectionError(e)

