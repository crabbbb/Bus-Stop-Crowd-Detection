from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bus
from .serializer import BusSerializer

# List all buses or create a new bus
class BusListView(APIView):
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific bus
class BusDetailView(APIView):
    def get_object(self, pk):
        try:
            return Bus.objects.get(pk=pk)
        except Bus.DoesNotExist:
            return None

    def get(self, request, pk):
        bus = self.get_object(pk)
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BusSerializer(bus)
        return Response(serializer.data)

    def put(self, request, pk):
        bus = self.get_object(pk)
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BusSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bus = self.get_object(pk)
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
