from django.db import models
from bson.objectid import ObjectId
from django.core.exceptions import ValidationError

class Route(models.Model) :
    # variable name will be the field name of the collection
    # data inside collections
    RouteId = models.CharField(max_length=5, primary_key=True)
    RouteDescription = models.TextField() 
    RouteDuration = models.IntegerField() # In minute 
    FromCampus = models.BooleanField()
    IsActive = models.BooleanField()

    # overwrite the original version
    def save(self, *args, **kwargs) :
        # id field is empty 
        if not self.RouteId :
            # create a new column for numeric id and sort it 
            last = Route.objects.annotate(numericId = models.functions.Cast(models.Substr('RouteId', 2), models.IntegerField())).order_by('-numericId').first()

            if last : 
                # get the next number of the last id
                lastId = int(last.id[1:])
                newId = lastId + 1

                if newId > 999:
                    raise ValidationError("ID cannot exceed 999 eg, 'A999'. Maximum limit reached. For more action please contact developer")
            else :
                newId = 1
            
            # eg, A001
            self.RouteId = f"R{newId:03d}"
        # call the original verion 
        super().save(*args, **kwargs)

    class Meta : 
        # custom collection name 
        db_table = "Route"
        # make the custome id also unique with the _id (object_id)
        unique_together = ('RouteId', )

    def __str__(self) :
        return f"object id > {self.id} (route id > {self.RouteId}, route description > {self.RouteDescription}, route duration > {self.RouteDuration}, from campus? > {self.FromCampus}, is active? > {self.IsActive})"