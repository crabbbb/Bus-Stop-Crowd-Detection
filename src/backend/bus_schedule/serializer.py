# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from bson import ObjectId

# for handle object id create by the mongodb
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value) if isinstance(value, ObjectId) else value

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId format.")

class BusSerializer(serializers.Serializer) :
    _id = ObjectIdField(required=False)
    BusId = serializers.CharField(allow_blank=True, required=False)
    CarPlateNo = serializers.CharField(allow_blank=False, required=False, max_length=7)
    Capacity = serializers.IntegerField(required=False, min_value=1)
    IsActive = serializers.IntegerField(required=False, min_value=0, max_value=1)

    # custom validation for Capacity
    def validate_Capacity(self, value):
        if value >= 0 and value <= 1:
            raise serializers.ValidationError("Capacity only can be Valid or Invalid")
        return value
    
class BusStationSerializer(serializers.Serializer) : 
    _id = ObjectIdField(required=False)
    StationId = serializers.CharField(allow_blank=True, required=False)
    StationName = serializers.CharField(allow_blank=True, required=False)

class RouteSerializer(serializers.Serializer) : 
    _id = ObjectIdField(required=False)
    RouteId = serializers.CharField(allow_blank=True, required=False)
    RouteDuration = serializers.IntegerField(required=False, min_value=1)
    FromCampus = serializers.IntegerField(required=False, min_value=0, max_value=1)
    IsActive = serializers.IntegerField(required=False, min_value=0, max_value=1)

class RouteStationSerializer(serializers.Serializer) : 
    _id = ObjectIdField(required=False)
    StationName = serializers.CharField(allow_blank=True, required=False)
    RouteId = serializers.CharField(allow_blank=True, required=False)
    RouteOrder = serializers.IntegerField(required=False, min_value=1)

class AssignmentSerializer(serializers.Serializer) : 
    _id = ObjectIdField(required=False)
    AssignmentId = serializers.CharField(allow_blank=True, required=False)
    Time = serializers.TimeField(format='%H:%M:%S', input_formats=['%H:%M:%S', '%I:%M %p'], required=False, allow_null=True)
    # sun = 0, mon = 1, ..., sat = 6
    DayOfWeek = serializers.IntegerField(required=False, min_value=0, max_value=6)
    BusId = serializers.CharField(allow_blank=True, required=False)
    RouteId = serializers.CharField(allow_blank=True, required=False)
