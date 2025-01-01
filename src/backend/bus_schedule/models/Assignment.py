from .supermodel import SuperModel

class Assignment(SuperModel) :
    __collection = "Assignment"
    __idHead = "A"
    
    def __init__(self):
        super().__init__(self.__collection, self.__idHead)