FIELD_SIZE = 50
# TODO: use enums everywhere
DIR_RIGHT = 0
DIR_UP = 1
DIR_LEFT = 2
DIR_DOWN = 3
move_pos = {
    DIR_RIGHT: lambda pos: (pos[0] + 1, pos[1]),
    DIR_DOWN: lambda pos: (pos[0], pos[1] + 1),
    DIR_LEFT: lambda pos: (pos[0] - 1, pos[1]),
    DIR_UP: lambda pos: (pos[0], pos[1] - 1),
    }