from .supermodel import SuperModel

class Route(SuperModel) :
    __collection = "Route"
    __idHead = "R"
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead)