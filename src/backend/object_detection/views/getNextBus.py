from datetime import datetime
from backend.utils import mongo
from bus_schedule.models import RouteStation, Bus

def _getCollection(collectionName) : 
    try :
        if not mongo.isHealthy() :
            # either no connect or connection down 
            if not mongo.reconnect() : 
                # unable to connect due to file problem 
                return None
        
        # have connection, get collection 
        db = mongo.getDB()
        return db[collectionName]
    except ConnectionError as e : 
        # for view to handle 
        raise ConnectionError(e) 

def getNextBus(stationName):
    try:
        # ------------------------------------------------
        # STEP 1: Get station _id based on stationName
        # ------------------------------------------------

        stationCollection = _getCollection("BusStation")
        if stationCollection is None:
            return None
        
        stationDoc = stationCollection.find_one({"StationName": stationName})
        print(f"station > {stationDoc}")
        if not stationDoc:
            print("Station not found")
            return None
        
        stationId = stationDoc["StationId"]  # or your unique ID field
        
        # ------------------------------------------------
        # STEP 2: Find all routes that pass through this station
        # ------------------------------------------------
        routeStation = RouteStation()  # your routeStation class
        # Example filter: all route-station docs with matching stationId
        # If you want only the routes where this station is the 1st stop, keep RouteOrder=1
        rsFilter = {
            "StationName": stationName,
            "RouteOrder": 1   
        }

        rsResult = routeStation.getByfilter(rsFilter)
        print(f"rsResult > {rsResult}")
        if not rsResult:
            print("No routes found for this station.")
            return None
        
        # Build a list (or set) of routeIds:
        # If each doc in rsResult has a field "RouteId", extract them:
        routeIds = [doc["RouteId"] for doc in rsResult]
        print(routeIds)
        if not routeIds:
            return None
        
        # ------------------------------------------------
        # STEP 3: Find the next bus times for those routes
        # ------------------------------------------------
        # Suppose your bus times are in "assignment" or "busSchedule" collection:
        assignementCollection = _getCollection("Assignment")
        if assignementCollection is None:
            return None
        
        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")
        dayOfWeek = now.weekday()  # 0=Monday, 6=Sunday
        
        timeQuery = {
            "RouteId": {"$in": routeIds},      # Only consider these routes
            "Time": {"$gte": currentTime},     # Time >= now
            "DayOfWeek": dayOfWeek+1            # same day-of-week
        }
        
        # We only want the earliest upcoming bus => sort by Time ascending
        nextBusRecord = assignementCollection.find_one(timeQuery, sort=[("Time", 1)])
        print(currentTime)
        print(nextBusRecord)
        if not nextBusRecord:
            # No upcoming bus for the day
            return None
        
        # nextBusRecord might look like: { "RouteId": ..., "BusId": ..., "Time": ... }
        busId = nextBusRecord["BusId"]
        
        # ------------------------------------------------
        # STEP 4: Retrieve the Bus info (capacity, etc.)
        # ------------------------------------------------
        bus = Bus()
        busCapacity = bus.getWithID(busId)
        
        # Return whichever info you need
        return nextBusRecord, busCapacity
    
    except ConnectionError as e:
        raise ConnectionError(e)
