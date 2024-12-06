# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from .models import Bus, Schedule, ScheduleAssignment, Assignment, BusStation, BusTrackingLog, Route, RouteStation

class BusSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Bus
        # __all__ can be understand as somethings like this ['id', 'name', 'capacity']
        fields = '__all__' 

class ScheduleSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Schedule
        fields = '__all__'

class ScheduleAssignmentSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = ScheduleAssignment
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Assignment
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