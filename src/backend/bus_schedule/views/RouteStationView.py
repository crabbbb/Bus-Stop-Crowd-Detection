from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import RouteStation, Route, BusStation
from ..serializer import RouteStationSerializer
from backend.utils import message

# if dont have then add in, if more than then delete 
class RouteStationListView(APIView) : 
    def post(self, request):
        try:
            # data passing format must be: 
            # {
            #   "RouteId": "R001", 
            #   "StationList": [
            #       {"stationName": "BusStop 4", "order": 1}, 
            #       {"stationName": "Wangsa Maju", "order": 2}
            #   ]
            # }

            # Validate request structure
            if not (
                request.data 
                and "RouteId" in request.data 
                and "StationList" in request.data 
                and isinstance(request.data["StationList"], list)
            ):
                # if format wrong -> 400 Bad Request
                return Response({"error": message.DATA_FORMAT}, status=status.HTTP_400_BAD_REQUEST)

            routeId = request.data["RouteId"]
            stationList = request.data["StationList"]

            # Fetch old data (from DB) to compare
            joinTable = RouteStation()
            oldList = joinTable.getWithID(idData=routeId)
            if oldList is None:
                # None indicates some internal or config error in getWithID
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Compare old vs new
            deleteList = []
            sameList = []  # (stationName, order) pairs that remain unchanged

            # oldList example: [{"RouteId": "R001", "StationName": "MRT", "RouteOrder": 1}, ...]
            # stationList example: [{"stationName": "BusStop 4", "order": 1}, ...]

            # Identify which old records need deletion (or are the same)
            for oldItem in oldList:
                oldStationName = oldItem["StationName"]
                oldOrder = oldItem["RouteOrder"]

                # See if there's a new item with the same station name
                newMatch = next(
                    (n for n in stationList if n["stationName"] == oldStationName),
                    None
                )
                if not newMatch:
                    # old station not found in the new list -> delete
                    deleteList.append(oldItem)
                else:
                    # found a new item with same station name -> check order
                    if newMatch["order"] != oldOrder:
                        # order changed -> delete old, will re-add new
                        deleteList.append(oldItem)
                    else:
                        # same station name, same order -> no changes needed
                        sameList.append({
                            "StationName": oldStationName,
                            "RouteOrder": oldOrder
                        })

            # Perform deletion
            for d in deleteList:
                joinTable.deleteOne(routeId, d["StationName"])

            # Add new stations 
            # only add if they are not in sameList (eg. truly new or changed order)
            for s in stationList:
                # Check if s is in sameList
                # sameList stores {"StationName": <>, "RouteOrder": <>}
                match = next(
                    (x for x in sameList 
                        if x["StationName"] == s["stationName"] 
                        and x["RouteOrder"] == s["order"]), 
                    None 
                )
                if not match:
                    # not in same list -> means need to create a new record
                    data = {
                        "RouteId": routeId,
                        "StationName": s["stationName"],
                        "RouteOrder": s["order"]
                    }
                    serializer = RouteStationSerializer(data=data)
                    if serializer.is_valid():
                        joinTable.createOne(data=serializer.validated_data)
            
            # Final check
            validate = joinTable.getWithID(routeId)  # get updated records
            if validate is None:
                return Response({"error": "Unexpected error retrieving final data"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if len(validate) == len(stationList):
                return Response({"success": len(stationList)}, 
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Unexpected error: expected {len(stationList)} records, but found {len(validate)} in the DB"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ConnectionError:
            return Response({"error": message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RouteStationDetailView(APIView) :
    def get(self, request, id) : 
        try :
            if id : 
                print(id)
                # have data
                joinTable = RouteStation()

                # using route to get the stationName 
                result = joinTable.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                serializer = RouteStationSerializer(result, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RouteStationUtility(APIView) :
    @staticmethod
    def sortDictionary(oriDict) : 
        return {key: oriDict[key] for key in sorted(oriDict)}
    
    @staticmethod
    def getHomePage(id : str) :
        return f"/route?RouteId={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/route/detail/{id}"