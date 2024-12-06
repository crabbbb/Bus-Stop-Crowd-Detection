from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class BusScheduleAssignment(models.Model) :
    # variable name will be the field name of the collection
    # this will handle the object id create by mongodb
    # auto generated, no need input 
    # id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))

    # data inside collections
    AssignmentId = models.CharField(max_length=5)
    ScheduleId = models.CharField(max_length=5)
    RouteId = models.CharField(max_length=5)
    BusId = models.CharField(max_length=5)

    # overwrite the original versio 
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.AssignmentId :
            # create a new column for numeric id and sort it 
            last = BusScheduleAssignment.objects.annotate(numericId = models.functions.Cast(models.Substr('AssignmentId', 2), models.IntegerField())).order_by('-numericId').first()

            if last : 
                # get the next number of the last id
                lastId = int(last.id[1:])
                newId = lastId + 1

                if newId > 999:
                    raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            else :
                newId = 1
            
            # eg, A001
            self.AssignmentId = f"A{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "BusScheduleAssignment"

    def __str__(self) :
        return f"object id > {self.id} ( assignment id > {self.AssignmentId}, schedule id > {self.ScheduleId}, route id > {self.RouteId}, bus id > {self.BusId})"