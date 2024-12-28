# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from .models.choices import TrueFalse
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
    IsActive = serializers.IntegerField(required=False, min_value=0)

    # custom validation for Capacity
    def validate_Capacity(self, value):
        if value >= 0 and value <= 1:
            raise serializers.ValidationError("Capacity only can be Valid or Invalid")
        return value