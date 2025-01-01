from .supermodel import SuperModel

class BusStation(SuperModel) :
    __collection = "BusStation"
    __idHead = "S"
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead, idName="StationId")