from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Route
from ..serializer import RouteSerializer
from backend.utils import message

# no need id to create 
class RouteListView(APIView) : 
    # get all 
    def get(self, request) :
        # if have request filter it 
        rid = request.query_params.get("RouteId")
        minDuration = request.query_params.get("MinDuration")
        maxDuration = request.query_params.get("MaxDuration")
        fromCampus = request.query_params.get("FromCampus")
        isActive = request.query_params.get("IsActive")

        filters = []

        if rid:
            filters.append({"RouteId": {"$regex": rid, "$options": "i"}})
        if minDuration:
            filters.append({"RouteDuration": {"$gte": int(minDuration)}})
        if maxDuration:
            filters.append({"RouteDuration": {"$lte": int(maxDuration)}})
        if fromCampus:
            filters.append({"FromCampus": int(fromCampus)})
        if isActive:
            filters.append({"IsActive": int(isActive)})

        query = {"$and": filters} if filters else {}
        
        # get data 
        try : 
            route = Route()
            routes = None
            
            # fill in data to buss
            if not query : 
                # filter is empty
                routes = route.getAll()
            else :
                # filter not empty 
                routes = route.getByfilter(query)
            
            if routes is None : 
                # file problem
                return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif not routes : 
                # empty list , database dont have data 
                return Response({"message": message.NOT_FOUND}, status=status.HTTP_200_OK)

            # have data 
            serializer = RouteSerializer(routes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request) : 
        try :
            # check validation of data by using serializer 
            serializer = RouteSerializer(data=request.data)

            if serializer.is_valid() : 

                route = Route()
                
                # if dont have problem get the data store into database 
                data = serializer.validated_data
                
                result = route.createOne(data=data)

                if result is None : 
                    # configuration file error 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # if all success 
                return Response({
                    "success" : f"{message.CREATE_SUCCESS}, ID : {data["RouteId"]}",
                    "redirect" : RouteUtility.getHomePage(data["RouteId"]),
                    "id" : data["RouteId"]
                }, status=status.HTTP_201_CREATED)
            else :
                # data doesnot valid 
                return Response({"error" : serializer.errors}, status=status.HTTP_200_OK)
        except ConnectionError as e :
            return Response({"error" : message.DATABASE_CONNECTION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RouteDetailView(APIView) :

    def get(self, request, id) : 

        try :
            if id : 
                # have data
                route = Route()

                # get the class 
                result = route.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                serializer = RouteSerializer(result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update 
    def put(self, request, id) : 
        try : 
            if id : 
                route = Route()

                # get the data 
                result = route.getWithID(id)
                
                # ensure id will always be same 
                if result["RouteId"] == request.data["RouteId"] : 

                    # check None
                    if result is None : 
                        return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # check empty 
                    if not result : 
                        # 404 page not found 
                        return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                    # have data 
                    # do validation checking 
                    serializer = RouteSerializer(data=request.data)

                    if serializer.is_valid() : 
                        # check same 
                        if result == serializer.validated_data : 
                            # old same with new data, no update required 
                            
                            return Response(
                                {
                                    "success": f"{message.NO_CHANGE_REQUIRED}",
                                    "redirect": RouteUtility.getDetailPage(serializer.data.get('RouteId'))
                                },
                                status=status.HTTP_200_OK
                            )
                        else : 
                            # different 
                            route.updateOne(updatedData=serializer.validated_data)
                            return Response(
                                {
                                    "success": f"{message.UPDATE_SUCCESS}, ID : {result["RouteId"]}",
                                    "redirect": RouteUtility.getHomePage(result["RouteId"])
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
        try : 
            if id : 
                route = Route()

                # get the data 
                result = route.getWithID(id)

                # check None
                if result is None : 
                    return Response({"error": message.CONFIGURATION_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # check empty 
                if not result : 
                    # 404 page not found 
                    return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                
                # have data 
                # perform delete 
                route.deleteOne(idData=id)
                return Response(
                    {
                        "success": f"{message.DELETE_SUCCESS}, ID : {result["RouteId"]}",
                        "redirect": RouteUtility.getHomePage(result["RouteId"])
                    }, 
                    status=status.HTTP_200_OK
                )
            else : 
                # dont have 
                return Response({"error": message.PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except ConnectionError as e : 
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RouteUtility(APIView) :
    
    @staticmethod
    def getHomePage(id : str) :
        return f"/route?id={id}"
    
    @staticmethod
    def getDetailPage(id : str) :
        return f"/route/detail/{id}"