# code below will bring help on serializer and de-serializer 
from rest_framework import serializers
from .models import Bus

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        # __all__ can be understand as somethings like this ['id', 'name', 'capacity']
        fields = '__all__' 