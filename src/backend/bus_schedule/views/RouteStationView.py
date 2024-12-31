from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import RouteStation, Route, BusStation
from ..serializer import RouteStationSerializer
from backend.utils import message

# if dont have then add in, if more than then delete 
class RouteStationListView(APIView) : 
    def post(self, request) : 
        try :
            # data passin format must be {RouteId : R001, StationList : {1 : "BusStop 4", 2 : "Wangsa Maju"}}
            # check the request.data format 
            if not (request.data and "RouteId" in request.data and "StationList" in request.data and type(request.data["StationList"]) == list) :
                # if format wrong raise 400 + error - 400 bad request 
                return Response({"error" : message.DATA_FORMAT}, status=status.HTTP_400_BAD_REQUEST)
            
            # sorting 
            # stationList = RouteStationUtility.sortDictionary(request.data["StationList"])
            # print(f"sorted > {stationList}")
            stationList = request.data["StationList"]


            # take value for compare 
            # if empty then no need to compare 
            joinTable = RouteStation()
            # will return a empty list if dont have match else None or error  
            result = joinTable.getWithID(idData=request.data["RouteId"])

            if result is None : 
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # old compare with new 
            deleteList = []
            sameList = []
            if result : 
                # result = old 
                # request.data = stationList = new 
                for r in result :
                    for s in stationList : 
                        if s["StationName"] == r["StationName"] :
                            if s["RouteOrder"] != r["RouteOrder"] :
                                # diff order same location - need to delete  
                                deleteList.append(r)
                                break
                            else : 
                                # same order same station
                                sameList.append({"StationName" : r["StationName"], "RouteOrder" : r["RouteOrder"]})
                        else : 
                            # diff station 
                            deleteList.append(r)
                            break
            
            # perform delete 
            for d in deleteList : 
                joinTable.deleteOne(d)

            # add value 
            for s in stationList : 
                cpy = {"StationName" : s["stationName"], "RouteOrder" : s["order"]}
                if cpy not in sameList : 
                    data = {
                        "RouteId" : request.data["RouteId"],
                        "StationName" : cpy["StationName"],
                        "RouteOrder" : cpy["RouteOrder"]
                    }
                # use serializer 
                serializer = RouteStationSerializer(data=data)

                if serializer.is_valid() : 
                    joinTable.createOne(data=serializer.validated_data)
            
            # final do compare , the just adding into database and the one pass in 
            validate = joinTable.getWithID(idData=request.data["RouteId"])
            if len(validate) == len(stationList) : 
                return Response({
                    "success" : len(stationList)
                }, status=status.HTTP_201_CREATED)
            else : 
                return Response({"error": f"Unexpected error happen, unable to added all data into database. Expected number of record > {len(stationList)}, Actual number of record > {len(validate)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ConnectionError as e :
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RouteStationDetailView(APIView) :
    def get(self, request, id) : 

        try :
            if id : 
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
                serializer = RouteStationSerializer(result)
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