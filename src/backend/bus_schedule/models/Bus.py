from .supermodel import SuperModel
from bson import ObjectId

class Bus(SuperModel) :
    __collection = "Bus"
    __idHead = "B"
    
    def __init__(self, BusId = None, CarPlateNo = None, Capacity = None, IsActive = None):
        super().__init__(self.__collection, self.__idHead)
        self.BusId = BusId if BusId else None
        self.CarPlateNo = CarPlateNo if CarPlateNo else None
        self.Capacity = Capacity if Capacity else None
        self.IsActive = IsActive if IsActive else None

    def getAllCarplate(self) :
        try :
            filterCondition = {}
            # no return _id but return column Carplateno 
            options = {"CarPlateNo": 1, "_id": 0}

            return super().getByfilter(filterCondition=filterCondition, options=options)
        except ConnectionError as e : 
            raise ConnectionError(e)

    def __str__(self) :
        return f"object id > {self.id} (bus id > {self.BusId}, car plate no > {self.CarPlateNo}, capacity > {self.Capacity}, is activte? > {self.IsActive})"