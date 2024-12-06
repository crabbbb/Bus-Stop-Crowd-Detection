from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class BusSchedule(models.Model) :
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
    # this will handle the object id create by mongodb
    # auto generated, no need input 
    # id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))

    # data inside collections
    ScheduleId = models.CharField(max_length=5)
    # datatype : datatime.time, only time no date 
    DepartureTime = models.TimeField()
    ArrivalTime = models.TimeField()
    DayOfWeek = models.IntegerField(choices=Day.choices)

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.ScheduleId :
            # create a new column for numeric id and sort it 
            last = BusSchedule.objects.annotate(numericId = models.functions.Cast(models.Substr('ScheduleId', 3), models.IntegerField())).order_by('-numericId').first()

            if last : 
                # get the next number of the last id
                lastId = int(last.id[2:])
                newId = lastId + 1

                if newId > 999:
                    raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            else :
                newId = 1
            
            # eg, A001
            self.ScheduleId = f"BS{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "BusSchedule"

    def __str__(self) :
        return f"object id > {self.id} ( schedule id > {self.ScheduleId}, departure time > {self.DepartureTime}, arrival time > {self.ArrivalTime}, day of week > {self.get_DayOfWeek_display()})"