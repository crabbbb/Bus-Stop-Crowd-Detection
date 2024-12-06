# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from .models import Bus, BusSchedule, BusScheduleAssignment, BusStation, BusTrackingLog, Route, RouteStation

class BusSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Bus
        # __all__ can be understand as somethings like this ['id', 'name', 'capacity']
        fields = '__all__' 

class BusScheduleSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = BusSchedule
        fields = '__all__'

class BusScheduleAssignmentSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = BusScheduleAssignment
        fields = '__all__'

class BusStationSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = BusStation
        fields = '__all__'

class BusTrackingLogSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = BusTrackingLog
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Route
        fields = '__all__'

class RouteStationSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = RouteStation
        fields = '__all__'