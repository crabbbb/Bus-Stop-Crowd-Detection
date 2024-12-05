from django.db import models
from bson.objectid import ObjectId

class Bus(models.Model) :
    # variable name will be the field name of the collection
    # this will handle the object id create by mongodb
    id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))

    # data inside collections
    BusId = models.CharField(max_length=5)
    CarPlateNo = models.CharField(max_length=7)
    Capacity = models.IntegerField()
    IsActive = models.BooleanField()

    # overwrite the original versio 
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.id :
            lastBus = Bus.objects.annotate(numericId = models.functions.Cast(models.Substr('BusId', 2), models.IntegerField())).order_by('-numericId').first()

            if lastBus : 
                # get the next number of the last id
                lastId = int(lastBus.id[1:])
                newId = lastId + 1
            else :
                newId = 1
            
            # eg, A001
            self.id = f"B{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "Bus"

    def __str__(self) :
        return self.name