# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from .models.choices import TrueFalse

class BusSerializer(serializers.Serializer) :
    BusId = serializers.CharField(allow_blank=True, required=False)
    CarPlateNo = serializers.CharField(allow_blank=False, required=False, max_length=7)
    Capacity = serializers.IntegerField(required=False, min_value=1)
    IsActive = serializers.IntegerField(required=False, min_value=0)

    # custom validation for Capacity
    def validate_Capacity(self, value):
        if value >= 0 and value <= 1:
            raise serializers.ValidationError("Capacity only can be Valid or Invalid")
        return value