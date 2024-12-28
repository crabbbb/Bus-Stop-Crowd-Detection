from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Bus
from ..serializer import BusSerializer
from backend.utils import message
from bson import ObjectId

# no need id to create 
class BusListView(APIView) : 
    # get all 
    def get(self, request) :
        print("Get Function active ")
        print("Query Params:", request.query_params)
        # if have request filter it 
        bid = request.query_params.get("BusId")
        carplate = request.query_params.get("CarPlateNo")
        minCapacity = request.query_params.get("MinCapacity")
        maxCapacity = request.query_params.get("MaxCapacity")
        isActive = request.query_params.get("IsActive")

        filters = []

        if bid:
            filters.append({"BusId": {"$regex": bid, "$options": "i"}})
        if carplate:
            filters.append({"CarPlateNo": {"$regex": carplate, "$options": "i"}})
        if minCapacity:
            filters.append({"Capacity": {"$gte": int(minCapacity)}})
        if maxCapacity:
            filters.append({"Capacity": {"$lte": int(maxCapacity)}})
        if isActive:
            filters.append({"IsActive": int(isActive)})

        query = {"$and": filters} if filters else {}
        
        # get data 
        try : 
            bus = Bus()
            buss = None
            
            # fill in data to buss
            if not query : 
                # filter is empty
                buss = bus.getAll()
            else :
                # filter not empty 
                buss = bus.getByfilter(query)
            
            if buss is None : 
                # file problem
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif not buss : 
                # empty list , database dont have data 
                return Response({"message": message.NOT_FOUND}, status=status.HTTP_200_OK)

            # have data 
            serializer = BusSerializer(buss, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request) : 
        print("POST function activate")
        print("Query Params:", request.query_params)
        print(request.data)
        try :
            # change carplate to uppercase 
            copyData = request.data.copy()

            if "CarPlateNo" in copyData:
                copyData["CarPlateNo"] = copyData["CarPlateNo"].upper()


            # check validation of data by using serializer 
            serializer = BusSerializer(data=copyData)

            if serializer.is_valid() : 
                # check carplate duplicate 
                bus = Bus()
                carplate = serializer.validated_data.get("CarPlateNo").upper()

                if bus.getByfilter({"CarPlateNo": carplate}) :
                    # Send ok because dont want detect as error 
                    return Response({"error": {
                        "CarPlateNo": f"{message.DUPLICATE_RECORD}, this Car Plate No already been register"
                    }}, status=status.HTTP_200_OK)
                
                # if carplate dont have problem get the data store into database 
                data = serializer.validated_data
                
                result = bus.createOne(data=data)

                if result is None : 
                    # configuration file error 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # if all success 
                return Response({
                    "success" : f"{message.CREATE_SUCCESS}, ID : {data["BusId"]}",
                    "redirect" : BusUtility.getHomePage(serializer.data.get('BusId'))
                }, status=status.HTTP_201_CREATED)
            else :
                # data doesnot valid 
                return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusDetailView(APIView) :

    def get(self, request, id) : 
        print("Get By ID Archieve")

        try :
            if id : 
                # have data
                bus = Bus()

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
                serializer = BusSerializer(result)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update 
    def put(self, request, id) : 
        print("Update function achieve")
        try : 
            if id : 
                bus = Bus()

                # get the data 
                result = bus.getWithID(id)
                
                # ensure id will always be same 
                if result["BusId"] == request.data["BusId"] : 

                    # check None
                    if result is None : 
                        return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # check empty 
                    if not result : 
                        # 404 page not found 
                        return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                    # have data 
                    # do validation checking 
                    serializer = BusSerializer(data=request.data)

                    if serializer.is_valid() : 
                        # check same 
                        if result == serializer.validated_data : 
                            # old same with new data, no update required 
                            print("here")
                            
                            return Response(
                                {
                                    "success": f"{message.NO_CHANGE_REQUIRED}",
                                    "redirect": BusUtility.getDetailPage(serializer.data.get('BusId'))
                                },
                                status=status.HTTP_200_OK
                            )
                        else : 
                            # different 
                            bus.updateOne(updatedData=serializer.validated_data)
                            return Response(
                                {
                                    "success": f"{message.UPDATE_SUCCESS}, ID : {result["BusId"]}",
                                    "redirect": BusUtility.getHomePage(result["BusId"])
                                },
                                status=status.HTTP_200_OK
                            )
                    else : 
                        # invalid format return 
                        return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
                else : 
                    # inconsistency data, raise error 
                    return Response({"error": message.INCONSISTENT_ID}, status=status.HTTP_400_BAD_REQUEST)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id) : 
        print("Delete function archieve")
        try : 
            if id : 
                bus = Bus()

                # get the data 
                result = bus.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                # perform delete 
                bus.deleteOne(idData=id)
                return Response(
                    {
                        "success": f"{message.DELETE_SUCCESS}, ID : {result["BusId"]}",
                        "redirect": BusUtility.getHomePage(result["BusId"])
                    }, 
                    status=status.HTTP_200_OK
                )
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusUtility(APIView) :

    # get carplate 
    def get(self, request) : 
        # check data is none or not 
        carplate = request.query_params.get('CarPlateNo', None)

        print("carplate", carplate)
        
        if not carplate :
            # send nothings 
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # have somethings 
        try : 
            bus = Bus()

            result = bus.getAllSimilar("CarPlateNo", carplate.upper(), {"CarPlateNo": 1, "_id": 0})

            if not result : 
                # list is empty 
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            # have data 
            # convert to dict
            result = [carplate for carplate in result]
            # put into serilizer pass to frontend 
            serializer = BusSerializer(result, many=True)

            print(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e: 
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def getHomePage(id : str) :
        return f"/bus?id={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/bus/detail/{id}"