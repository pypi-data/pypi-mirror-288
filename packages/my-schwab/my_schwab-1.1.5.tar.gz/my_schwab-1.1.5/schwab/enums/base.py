from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def from_value(cls, value):
        if value is None:
            return value
        return cls(value).name