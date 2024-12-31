from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import BusStation
from ..serializer import BusStationSerializer
from backend.utils import message

class BusStationListView(APIView) : 
    # get all 
    def get(self, request) :
        print("Get Function active ")
        print("Query Params:", request.query_params)
        # if have request filter it 
        sid = request.query_params.get("StationName")
        isActive = request.query_params.get("IsActive")

        filters = []

        if sid:
            filters.append({"BusId": {"$regex": sid, "$options": "i"}})
        if isActive:
            filters.append({"IsActive": int(isActive)})

        query = {"$and": filters} if filters else {}
        
        # get data 
        try : 
            station = BusStation()
            stations = None
            
            # fill in data to buss
            if not query : 
                # filter is empty
                stations = station.getAll()
            else :
                # filter not empty 
                stations = station.getByfilter(query)
            
            if stations is None : 
                # file problem
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif not stations : 
                # empty list , database dont have data 
                return Response({"message": message.NOT_FOUND}, status=status.HTTP_200_OK)

            # have data 
            serializer = BusStationSerializer(stations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request) : 
        print("POST function activate")
        print("Query Params:", request.query_params)
        print(request.data)
        try :
            # check validation of data by using serializer 
            serializer = BusStationSerializer(data=request.data)

            if serializer.is_valid() : 

                station = BusStation()

                # stationName cannot duplicate 
                if station.getByfilter({"StationName": serializer.validated_data.get("StationName")}) :
                    # Send ok because dont want detect as error 
                    return Response({"error": {
                        "StationName": f"{message.DUPLICATE_RECORD}, this Station already been register"
                    }}, status=status.HTTP_200_OK)
                
                # if stationName dont have problem get the data store into database 
                data = serializer.validated_data
                
                result = station.createOne(data=data)

                if result is None : 
                    # configuration file error 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # if all success 
                return Response({
                    "success" : f"{message.CREATE_SUCCESS}, ID : {data["StationName"]}",
                    "redirect" : BusStationUtility.getHomePage(serializer.data.get("StationName"))
                }, status=status.HTTP_201_CREATED)
            else :
                # data doesnot valid 
                return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusStationDetailView(APIView) :    
    # update (activate or deactivate)
    def put(self, request, id) : 
        print("Update function achieve")
        try : 
            if id : 
                station = BusStation()

                # get the data 
                result = station.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                # change true to false or false to true
                result["IsActive"] = 0  if result["IsActive"] == 1 else 0
                serializer = BusStationSerializer(data=result)
                result = station.updateOne(updatedData=serializer.validated_data)

                return Response(
                    {
                        "success": f"{message.UPDATE_SUCCESS}, ID : {result["StationName"]}",
                        "redirect": BusStationUtility.getHomePage(result["StationName"])
                    },
                    status=status.HTTP_200_OK
                )
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id) : 
        print("Delete function archieve")
        try : 
            if id : 
                station = BusStation()

                # get the data 
                result = station.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                # perform delete 
                station.deleteOne(idData=id)
                return Response(
                    {
                        "success": f"{message.DELETE_SUCCESS}, ID : {result["StationName"]}",
                        "redirect": BusStationUtility.getHomePage(result["StationName"])
                    }, 
                    status=status.HTTP_200_OK
                )
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusStationUtility(APIView) :
    
    @staticmethod
    def getHomePage(id : str) :
        return f"/station?stationName={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/station/detail/{id}"