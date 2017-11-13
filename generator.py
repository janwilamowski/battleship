import random
from constants import DIR, move_pos
from Ship import Ship


def place_ships(board, shipCountBySize, is_mine=True):
    """
    approach: it would be safer (but slower) to calculate all remaining ship positions and then
    pick one randomly instead of brute forcing your way to a valid solution
    but this might not be necessary if the provided board space is big enough for all the ships
    """
    ship_area = 3 * sum(a*b for (a, b) in shipCountBySize.items()) + 6 * sum(shipCountBySize.values())
    board_area = board.width * board.height
    if ship_area > board_area:
        print('Warning: may not be able to place all ships')

    random.seed()
    ships = []
    space = set(board.grid.keys())
    neighbors = set()
    for size in sorted(shipCountBySize.keys(), reverse=True):
        if size > board.width and size > board.height:
            continue
        amount = shipCountBySize[size]
        for i in range(amount):
            max_tries = 20 # emergency break TODO can possibly be reduced
            for i in range(max_tries):
                rdir = random.randint(0, 1) # TODO: also use LEFT & UP if space is available
                max_x = board.width-size if rdir is 0 else board.width-1
                max_y = board.height-size if rdir is 1 else board.height-1
                free_fields = set(coords for coords in space if is_within(coords, max_x, max_y)).difference(neighbors)
                if len(free_fields) == 0:
                    print('no space left')
                    continue # TODO: many unneeded iterations. Try all options for rdir instead

                (x, y) = random.choice(list(free_fields))
                direction = DIR.RIGHT if rdir is 0 else DIR.DOWN
                pos = (x, y)
                fields = []

                for i in range(size):
                    if not pos in space or pos in neighbors: break
                    fields.append(board[pos])
                    space.remove(pos)
                    pos = move_pos[direction](pos)

                new_neighbors = get_neighbors((x, y), size, direction, board)
                touches_other_ship = not new_neighbors.issubset(space)
                neighbors.update( new_neighbors )
                if len(fields) is not size or touches_other_ship: # couldn't fit all ship fields
                    for field in fields:
                        space.add(field.position) # release for future use
                    continue

                # if it fits, it sits
                ship = Ship(board, size, (x, y), direction, is_mine)
                ships.append(ship)
                break
            else:
                print('unable to place ship of size {s}, aborting'.format(s=size))
                pr(board, space)
                continue
    return ships

def pr(board, space):
    """ debugging helper that outputs an ASCII board with its ships """
    for h in range(board.height):
        print(''.join('.' if (w, h) in space else 'X' for w in range(board.width)))
    print('--------------------')

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
