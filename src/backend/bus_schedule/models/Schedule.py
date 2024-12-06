from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class Schedule(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    ScheduleId = models.CharField(max_length=5, primary_key=True)
    IsActive = models.BooleanField()
    CreateAt = models.DateTimeField(auto_now=True)

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.ScheduleId :
            # create a new column for numeric id and sort it 
            last = Schedule.objects.annotate(numericId = models.functions.Cast(models.Substr('ScheduleId', 2), models.IntegerField())).order_by('-numericId').first()

            if last : 
                # get the next number of the last id
                lastId = int(last.id[1:])
                newId = lastId + 1

                if newId > 999:
                    raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            else :
                newId = 1
            
            # eg, A001
            self.ScheduleId = f"S{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "Schedule"
        # make the custome id also unique with the _id (object_id)
        unique_together = ('ScheduleId', )

    def __str__(self) :
        return f"object id > {self.id} (schedule id > {self.ScheduleId}, is active? > {self.IsActive}, create at > {self.CreateAt})"