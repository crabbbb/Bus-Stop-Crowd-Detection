from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class BusStation(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    StationId = models.CharField(max_length=5, blank=True, null=True)
    StationName = models.CharField(max_length=255)
    IsActive = models.BooleanField()

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.StationId :
            # create a new column for numeric id and sort it 
            last = BusStation.objects.annotate(numericId = models.functions.Cast(models.Substr('StationId', 2), models.IntegerField())).order_by('-numericId').first()

            if last : 
                # get the next number of the last id
                lastId = int(last.id[1:])
                newId = lastId + 1

                if newId > 999:
                    raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            else :
                newId = 1
            
            # eg, A001
            self.StationId = f"S{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "BusStation"

    def __str__(self) :
        return f"object id > {self.id} (station id > {self.StationId}, station name > {self.StationName}, is active? > {self.IsActive})"