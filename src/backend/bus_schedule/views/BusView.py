from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Bus
from ..serializer import BusSerializer
from backend.utils import message
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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

        # get all bus from database 
        buss = Bus.objects.all()
        print(bid)
        if buss.exists() : 
            print("exist")
            if bid :
                # filter id 
                buss = buss.filter(BusId__icontains=bid)
            if carplate : 
                # filter carplate 
                buss = buss.filter(CarPlateNo__icontains=carplate)
            if minCapacity : 
                # convert capacity to int 
                minCapacity = int(minCapacity)
                # greter than equal 
                buss = buss.filter(Capacity__gte=minCapacity)
            if maxCapacity : 
                maxCapacity = int(maxCapacity)
                # less than equal 
                buss = buss.filter(Capacity__lte=maxCapacity)
            if isActive : 
                # change format 
                isActive = int(isActive)
                # filter isActive 
                buss = buss.filter(IsActive=isActive)
            
            if buss.exists() : 
                # after filter still have data 
                serializer = BusSerializer(buss, many=True)
                print(f"{serializer.data}")
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": message.NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    
    # create
    @method_decorator(ensure_csrf_cookie, name="dispatch")
    def post(self, request) :
        
        serializer = BusSerializer(data=request.data)

        # will check the attribute format, min max and is empty or not - all will return false 
        if serializer.is_valid() : 
            # car plate check duplicate 
            carplate = serializer.validated_data.get("CarPlateNo")
            if not BusUtility.isCarPlateExist(carplate) :
                serializer.save()
                return Response(
                        {
                            "success": f"{message.CREATE_SUCCESS}, ID : {serializer.data.get('BusId')}",
                            "redirect": f"/bus?id={serializer.data.get('BusId')}"
                        },
                        status=status.HTTP_201_CREATED)
            else : 
                # duplicate carplate
                return Response({"error": f"{message.DUPLICATE_RECORD}, Car Plate No {carplate} Exist"}, status=status.HTTP_400_BAD_REQUEST)
        else : 
            # dont have pass the checking condition, access serializer error message dict 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BusDetailView(APIView) :
    def getObject(self, id) :
        print("Get Function active2")
        try : 
            return Bus.objects.get(BusId=id)
        except ObjectDoesNotExist as e : 
            raise ObjectDoesNotExist(e)
        except MultipleObjectsReturned as e :
            raise MultipleObjectsReturned(e)

    def get(self, request, id) :
        
        try : 
            bus = self.getObject(id) 
            serializer = BusSerializer(bus)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e : 
            return Response({"error": f"{message.NOT_FOUND}, {e}"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e :
            return Response({"error": f"{message.DUPLICATE_RECORD}, {e}"}, status=status.HTTP_400_BAD_REQUEST)

    # update 
    def put(self, request, id) : 
        try : 
            bus = self.getObject(id) 
            # (originalData, theDataWantToUpdate)
            serializer = BusSerializer(bus, data=request.data)

            if serializer.is_valid() :
                # check do 2 data is match or not 
                if serializer.data == serializer.validated_data : 
                    # old same with new data, no update required 
                    return Response(
                            {
                                "success": f"{message.NO_UPDATE_REQUIRED}",
                                "redirect": f"/bus?id={serializer.data.get('BusId')}"
                            },
                            status=status.HTTP_200_OK)
                
                # check carplate exist or not 
                carplate = serializer.validated_data.get("CarPlateNo")
                
                if not BusUtility.isCarPlateExist(carplate) or (BusUtility.isCarPlateExist(carplate) and serializer.data.get("CarPlateNo") == carplate) : 
                    # car plate is in correct way 
                    serializer.save()
                    return Response(
                            {
                                "success": f"{message.UPDATE_SUCCESS}",
                                "redirect": f"/bus?id={serializer.data.get('BusId')}"
                            },
                            status=status.HTTP_200_OK)
                else :
                    # duplicate carplate
                    return Response({"error": f"{message.DUPLICATE_RECORD}, Car Plate No {carplate} Already Exist"}, status=status.HTTP_400_BAD_REQUEST)
            else : 
                # formating problem 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e : 
            return Response({"error": f"{message.NOT_FOUND}, {e}"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e :
            return Response({"error": f"{message.DUPLICATE_RECORD}, {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id) :
        try : 
            bus = self.getObject(id)
            bus.delete()
            return Response(
                        {
                            "success": f"{message.DELETE_SUCCESS}, ID : {id}",
                            "redirect": f"/bus?id={id}"
                        },
                        status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e : 
            return Response({"error": f"{message.NOT_FOUND}, {e}"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e :
            return Response({"error": f"{message.DUPLICATE_RECORD}, {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
class BusUtility() : 
    def isCarPlateExist(carplate: str) : 
        return Bus.objects.filter(CarPlateNo=carplate).exists()

