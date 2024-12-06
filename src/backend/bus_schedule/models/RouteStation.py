from django.db import models
from bson.objectid import ObjectId

class RouteStation(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    StationId = models.CharField(max_length=5)
    RouteId = models.CharField(max_length=5) 
    RouteOrder = models.IntegerField()

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # because both are fk so no need to generate any id 
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "RouteStation"

    def __str__(self) :
        return f"object id > {self.id} (station id > {self.StationId}, route id > {self.RouteId}, route order > {self.RouteOrder})"