from enum import Enum

FIELD_SIZE = 50

class DIR(Enum):
    """ Direction of ships and movements. Values represent angles in degrees. """
    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270
