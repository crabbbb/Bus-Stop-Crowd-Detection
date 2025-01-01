from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import BusStation
from ..serializer import BusStationSerializer
from backend.utils import message

class BusStationListView(APIView) : 
    # get all 
    def get(self, request) :
        print(request.query_params)
        # if have request filter it 
        stationId = request.query_params.get("StationId")
        stationName = request.query_params.get("StationName")

        filters = []

        if stationId:
            filters.append({"StationId": {"$regex": stationId, "$options": "i"}})
        if stationName:
            filters.append({"StationName": {"$regex": stationName, "$options": "i"}})

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
                    "success" : f"{message.CREATE_SUCCESS}, ID : {data["StationId"]}",
                    "redirect" : BusStationUtility.getHomePage(serializer.data.get("StationId"))
                }, status=status.HTTP_201_CREATED)
            else :
                # data doesnot valid 
                return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusStationDetailView(APIView) :  
    def get(self, request, id) : 
        try :
            if id : 
                # have data
                bus = BusStation()

                # get the class 
                result = bus.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                serializer = BusStationSerializer(result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update (activate or deactivate)
    def put(self, request, id) : 
        print("Update function achieve")
        print(request.data)
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
                serializer = BusStationSerializer(data=request.data)

                if serializer.is_valid() :
                    result = station.updateOne(updatedData=serializer.validated_data)

                    return Response(
                        {
                            "success": f"{message.UPDATE_SUCCESS}, ID : {result["StationId"]}",
                            "redirect": BusStationUtility.getHomePage(result["StationId"])
                        },
                        status=status.HTTP_200_OK
                    )
                else : 
                    return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
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
    # get stationName 
    def get(self, request) : 
        # check data is none or not 
        stationName = request.query_params.get('StationName', None)
        
        if not stationName :
            # send nothings 
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # have somethings 
        try : 
            station = BusStation()

            result = station.getAllSimilar("StationName", stationName, {"StationName": 1, "_id": 0})

            if not result : 
                # list is empty 
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            # have data 
            # convert to dict
            result = [station for station in result]
            # put into serilizer pass to frontend 
            serializer = BusStationSerializer(result, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e: 
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def getHomePage(id : str) :
        return f"/busStation?stationName={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/station/detail/{id}"