from enum import Enum

class TrueFalse(Enum):
    ACTIVE = 0
    INACTIVE = 1

    def __str__(self) :
        return self.value