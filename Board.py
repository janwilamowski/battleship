import pygame
import random
from Field import Field
from constants import DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT, FIELD_SIZE, move_pos


class Board():
    def __init__(self, width, height, screen, position=(0, 0), visible=False):
        self.height = height
        self.heightPx = height * FIELD_SIZE
        self.width = width
        self.widthPx = width * FIELD_SIZE
        self.screen = screen
        self.position = position

        # TODO: use NumPy array instead of nested lists?
        self.grid = dict([((x, y), Field(screen, (x, y), visible))
                for x in range(width) for y in range(height)])

    def uncover(self, position):
        self.grid[position].show()

    def uncoverPixels(self, position):
        self.grid[(position[0]/FIELD_SIZE, position[1]/FIELD_SIZE)].show()

    def uncover_all(self):
        for field in self.grid.values():
            field.show()

    def display(self):
        for coords, field in self.grid.iteritems():
            field.display(self.position)

    # def ship_fits(self, size, position, direction):
    #     avail_grid = [True for x in range(self.width) for y in range(self.height)]
    #     fields = []
    #     for i in range(size):
    #         pass # TODO
    #     return self.ship_fits_rec(avail_grid, size, position, direction)

    # def ship_fits_rec(self, grid, size, position, direction):
    #     if size == 1:
    #         if grid[position]:
    #             grid[position] = False
    #             return true
    #             # TODO: undo previous steps if doesn't fit or check all fields at once
    #     return self.ship_fits_rec(self, grid, size - 1, move_pos[direction](position))

    def add_ship(self, ship):
        offset = 0
        for field in ship.fields:
            pos = field.position
            if pos not in self.grid:
                print("field {f} isn't in this board".format(f=pos))
                continue
            field.smoke = True
            self[pos].ship = ship
            rect = pygame.Rect(offset, 0, FIELD_SIZE, FIELD_SIZE)
            surface = pygame.Surface(rect.size).convert()
            surface.blit(ship.image, (0, 0), rect)
            self[pos].image = pygame.transform.rotate(surface, ship.direction * 90)
            offset += FIELD_SIZE

    def shoot_random(self):
        targets = [pos for pos in self.grid.keys() if self[pos].visible]
        # TODO: exclude fields around known ships
        # TODO: try around partial hits first
        target = self[random.choice(targets)]
        if target.ship is not None:
            # target.smoke = False # TODO: should be the other way around
            target.ship.show(target)
            print("hit " + str(target.ship) + ", " + str(target.ship.discovered))
        else:
            target.visible = False


    def get_neighbor(self, position, direction):
        if direction == DIR_UP:
            neighbor_pos = (position[0], position[1] - 1)
        elif direction == DIR_DOWN:
            neighbor_pos = (position[0], position[1] + 1)
        elif direction == DIR_RIGHT:
            neighbor_pos = (position[0] + 1, position[1])
        elif direction == DIR_LEFT:
            neighbor_pos = (position[0] - 1, position[1])
        else:
            print("ERROR: can't move towards direction " + direction)
        if not 0 <= neighbor_pos[0] <= self.width or not 0 <= neighbor_pos[1] <= self.height:
            raise ValueError("requested neighbor of {pos} towards {dir} out of bounds".format(pos=position, dir=direction))
        return neighbor_pos

    def __getitem__(self, key):
        return self.grid[key]
