import pygame
import random
from Field import Field
from constants import FIELD_SIZE, BOARD_WIDTH, BOARD_HEIGHT


class Board():
    def __init__(self, width, height, screen, offset=(0, 0)):
        self.height = height
        self.heightPx = height * FIELD_SIZE
        self.width = width
        self.widthPx = width * FIELD_SIZE
        self.screen = screen
        self.offset = offset

        self.reset_fields()

    def uncover(self, position):
        return self.shoot(position)

    def uncoverPixels(self, position):
        pos_x = (position[0] - self.offset[0]) / FIELD_SIZE
        pos_y = (position[1] - self.offset[1]) / FIELD_SIZE
        if 0 <= pos_x < BOARD_WIDTH and 0 <= pos_y < BOARD_HEIGHT:
            return self.shoot((pos_x, pos_y))
        else:
            return None, None # ignore

    def uncover_all(self):
        for field in self.grid.values():
            field.show()

    def reset_fields(self):
        self.grid = dict([((x, y), Field(self.screen, (x, y)))
                for x in range(self.width) for y in range(self.height)])

    def display(self):
        for coords, field in self.grid.iteritems():
            field.display(self.offset)

    def add_ship(self, ship):
        offset = 0
        for field in ship.fields:
            pos = field.position
            if pos not in self.grid:
                print("field {f} isn't in this board".format(f=pos))
                continue
            self[pos].ship = ship
            rect = pygame.Rect(offset, 0, FIELD_SIZE, FIELD_SIZE)
            surface = pygame.Surface(rect.size).convert()
            surface.blit(ship.image, (0, 0), rect)
            self[pos].image = pygame.transform.rotate(surface, ship.direction.value)
            offset += FIELD_SIZE

    def shoot_random(self):
        targets = [pos for pos in self.grid.keys() if not self[pos].visible]
        return self.shoot(random.choice(targets))

    def shoot(self, coords):
        """ Uncovers the field at the given coordinates.
            Returns True if a ship was hit and False otherwise. Updates the ship if it was hit.
        """
        if not coords in self.grid or self.grid[coords].visible: return None, None

        target = self[coords]
        target.visible = True
        if target.ship is not None:
            sunk = target.ship.show(target)
            return True, target.ship
        return False, None

    def __getitem__(self, key):
        return self.grid[key]
