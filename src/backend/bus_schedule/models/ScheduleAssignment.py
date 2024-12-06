from django.db import models
from bson.objectid import ObjectId

class ScheduleAssignment(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    ScheduleId = models.CharField(max_length=5)
    AssignmentId = models.CharField(max_length=5) 

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # because both are fk so no need to generate any id 
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "ScheduleAssignment"

    def __str__(self) :
        return f"object id > {self.id} (schedule id > {self.ScheduleId}, assignment id > {self.AssignmentId})"