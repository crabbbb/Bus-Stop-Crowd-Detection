from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class Assignment(models.Model) :
    # DayOfWeek = BusSchedule.Day.SUNDAY
    class Day(models.IntegerChoices) :
        SUNDAY =  0, "SUNDAY"
        MONDAY = 1, "MONDAY"
        TUESDAY = 2, "TUESDAY"
        WEDNESDAY = 3, "WEDNESDAY"
        THURSDAY = 4, "THURSDAY"
        FRIDAY = 5, "FRIDAY"
        SATURDAY = 6, "SATURDAY"
    
    # variable name will be the field name of the collection
    # data inside collections
    AssignmentId = models.CharField(max_length=5, blank=True, null=True)
    Time = models.TimeField()
    DayOfWeek = models.IntegerField(choices=Day.choices)
    BusId = models.CharField(max_length=5)
    RouteId = models.CharField(max_length=5)

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.AssignmentId :
            # create a new column for numeric id and sort it 
            last = Assignment.objects.annotate(numericId = models.functions.Cast(models.Substr('AssignmentId', 2), models.IntegerField())).order_by('-numericId').first()

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
        db_table = "Assignment"

    def __str__(self) :
        return f"object id > {self.id} (assignment id > {self.AssignmentId}, time > {self.Time}, day of week > {self.get_DayOfWeek_display()}, bus id > {self.BusId}, route id {self.RouteId})"