from enum import Enum

FIELD_SIZE = 50

class DIR(Enum):
    """ Direction of ships and movements. Values represent angles in degrees. """
    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270

move_pos = {
    DIR.RIGHT: lambda pos: (pos[0] + 1, pos[1]),
    DIR.DOWN: lambda pos: (pos[0], pos[1] + 1),
    DIR.LEFT: lambda pos: (pos[0] - 1, pos[1]),
    DIR.UP: lambda pos: (pos[0], pos[1] - 1),
}
