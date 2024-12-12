from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models.functions import Substr, Cast
from ._TrueFalse import _TrueFalse

class Bus(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    BusId = models.CharField(max_length=5, blank=True, null=True)
    CarPlateNo = models.CharField(max_length=7)
    Capacity = models.IntegerField()
    IsActive = models.IntegerField(choices=_TrueFalse.choices, default=_TrueFalse.ACTIVE)

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.BusId :
            # create a new column for numeric id and sort it 
            ids = Bus.objects.values_list('BusId', flat=True)
            numericIds = [int(id[1:]) for id in ids if id[1:].isdigit()]

            lastId = max(numericIds, default=1)

            # get the next number of the last id
            if lastId > 1 :
                lastId = lastId + 1

            if lastId > 999:
                raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            
            # eg, A001
            self.BusId = f"B{lastId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "Bus"

    def __str__(self) :
        return f"object id > {self.id} (bus id > {self.BusId}, car plate no > {self.CarPlateNo}, capacity > {self.Capacity}, is activte? > {self.IsActive})"