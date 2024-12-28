from backend.utils import mongo
from django.http import StreamingHttpResponse, JsonResponse
from backend.utils import message
import json 
from enum import Enum

class Operation(Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"

    def __str__(self) :
        return self.value


def __getCollection(collectionName : str) :
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

def BusMonitor(request) : 
    try : 
        # get collection 
        collection = __getCollection("Bus")
        def evenStream() : 
            with collection.watch() as stream : 
                for change in stream : 
                    yield f"data: {json.dumps(change, default=str)}\n\n"

        return StreamingHttpResponse(evenStream(), content_type="text/event-stream")
    except ConnectionError as e : 
        return JsonResponse({"error": f"{message.DATABASE_CONNECTION_ERROR}, {e}"}, status=500)
    except Exception as e : 
        return JsonResponse({"error": f"Unexpected error occurs, {e}"}, status=500)
