from constants import DIR

move_pos = {
    DIR.RIGHT: lambda pos: (pos[0] + 1, pos[1]),
    DIR.DOWN: lambda pos: (pos[0], pos[1] + 1),
    DIR.LEFT: lambda pos: (pos[0] - 1, pos[1]),
    DIR.UP: lambda pos: (pos[0], pos[1] - 1),
}

def is_within(p, max_x, max_y):
    return p[0] <= max_x and p[1] <= max_y

def get_neighbors_ship(ship, board):
    return get_neighbors(ship.fields[0].position, ship.size, ship.direction, board)

def get_neighbors(pos, size, direction, board):
    h = board.height
    w = board.width
    candidates = set()
    for i in range(size):
        if i in [0, size-1]:
            candidates.update( get_diagonal_neighbors(pos) )
        if i is 0:
            candidates.add( move_pos[get_opposite_direction(direction)](pos) )
        if i is size-1:
            candidates.add( move_pos[direction](pos) )
        candidates.update( [ move_pos[d](pos) for d in get_vertical_directions(direction) ] )
        pos = move_pos[direction](pos)
    return set(c for c in candidates if 0 <= c[0] < w and 0 <= c[1] < h)

def get_diagonal_neighbors(coords):
    return (
        (coords[0]-1, coords[1]+1),
        (coords[0]+1, coords[1]+1),
        (coords[0]-1, coords[1]-1),
        (coords[0]+1, coords[1]-1)
    )

def get_orthogonal_neighbors(coords):
    return tuple(move_pos[d](coords) for d in DIR)

def get_vertical_directions(direction):
    if direction in (DIR.UP, DIR.DOWN):
        return (DIR.LEFT, DIR.RIGHT)
    else:
        return (DIR.UP, DIR.DOWN)

def get_opposite_direction(direction):
    if direction is DIR.RIGHT: return DIR.LEFT
    elif direction is DIR.LEFT: return DIR.RIGHT
    elif direction is DIR.UP: return DIR.DOWN
    elif direction is DIR.DOWN: return DIR.UP
