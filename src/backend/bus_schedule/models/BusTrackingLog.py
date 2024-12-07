from django.db import models
from bson.objectid import ObjectId

class BusTrackingLog (models.Model) :
    class Status (models.TextChoices) :
        HAVENT_ARRIVE = "HA", "HAVENT ARRIVE"
        ARRIVE = "A", "ARRIVE"
        DROP = "D", "DROPING"
        REST = "R", "RESTING"
        WAITING = "W", "WAITING"

    class Capacity (models.TextChoices) : 
        EMPTY = "E", "EMPTY" # 0%
        LOW = "L", "LOW" # 1-40% 
        MODERATE = "M", "MODERATE" # 41-70%
        ALMOST_FULL = "AF", "ALMOST FULL" # 71-99%
        FULL = "F", "FULL" # 100%

    # variable name will be the field name of the collection
    # this will handle the object id create by mongodb
    # auto generated, no need input 
    # id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))

    # data inside collections
    ArrivalDateTime = models.DateTimeField(blank=True, null=True)
    AssignmentId = models.CharField(max_length=5) 
    BusStatus = models.CharField(max_length=5, choices=Status.choices)
    BusCapacityEstimate = models.CharField(max_length=5, choices=Capacity.choices, blank=True, null=True)

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # because both are fk so no need to generate any id 
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "BusTrackingLog"

    def __str__(self) :
        return f"object id > {self.id} (arrival datetime > {self.ArrivalDateTime}, assignment id > {self.AssignmentId}, bus status > {self.get_BusStatus_display()}, bus capacity estimate > {self.get_BusCapacityEstimate_display()})"