from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.Bus import Bus
from serializer import BusSerializer
from backend.utils import message
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# no need id to create 
class BusListView(APIView) : 
    # get all 
    def get(self, request) :
        # if have request filter it 
        bid = request.query_params.get("BusId")
        carplate = request.query_params.get("CarPlateNo")
        capacity = request.query_params.get("Capacity")
        isActive = request.query_params.get("IsActive")

        # get all bus from database 
        buss = Bus.objects.all()

        if buss.exists() : 
            if bid :
                # filter id 
                buss = buss.filter(BusId=bid)
            if carplate : 
                # filter carplate 
                buss = buss.filter(CarPlateNo=carplate)
            if capacity : 
                # convert capacity to int 
                capacity = int(capacity)
                # filter capacity 
                buss = buss.filter(Capacity=capacity)
            if isActive : 
                # change format 
                isActive = isActive.upper()
                # filter isActive 
                buss = buss.filter(IsActive=isActive == "TRUE")
            
            if buss.exists() : 
                # after filter still have data 
                serializer = BusSerializer(data=buss, many=True)
                return Response(serializer.data)
        
        return Response({"not_found": message.NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    
    # create
    @method_decorator(ensure_csrf_cookie, name="dispatch")
    def post(self, request) :
        serializer = BusSerializer(data=request.data)

        # will check the attribute format, min max and is empty or not - all will return false 
        if serializer.is_valid() : 
            # car plate check duplicate 
            carplate = serializer.validated_data.get("CarPlateNo")
            if not Bus.objects.filter(CarPlateNo=carplate).exists() :
                serializer.save()
                return Response({"redirect": f"/bus?id={serializer.data.get('BusId')}"}, status=status.HTTP_201_CREATED)
            else : 
                # duplicate carplate
                return Response({"bad_request": f"{message.DUPLICATE_RECORD}, Car Plate No {carplate} Exist"}, status=status.HTTP_400_BAD_REQUEST)
        else : 
            # dont have pass the checking condition, access serializer error message dict 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BusDetailView(APIView) :
    def getObject(self, id) :
        try : 
            return Bus.objects.get(BusId=id)
        except ObjectDoesNotExist as e : 
            raise ObjectDoesNotExist(e)
        except MultipleObjectsReturned as e :
            raise MultipleObjectsReturned(e)

    def get(self, request, id) :
        try : 
            bus = self.getObject(id) 
            serializer = BusSerializer(data=bus)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e : 
            return Response({"not_found": f"{message.NOT_FOUND}, {e}"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e :
            return Response({"bad_request": f"{message.DUPLICATE_RECORD}, {e}"}, status=status.HTTP_400_BAD_REQUEST)

    # update - stop here, problem the different between have data= or dont have at BusSerializer 
    def put(self, request, id) : 
        try : 
            bus = self.getObject(id) 
            serializer = BusSerializer(data=bus)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e : 
            return Response({"not_found": f"{message.NOT_FOUND}, {e}"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e :
            return Response({"bad_request": f"{message.DUPLICATE_RECORD}, {e}"}, status=status.HTTP_400_BAD_REQUEST)

