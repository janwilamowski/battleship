import pygame
import random
from Field import Field
from constants import FIELD_SIZE


class Board():
    def __init__(self, width, height, screen, position=(0, 0)):
        self.height = height
        self.heightPx = height * FIELD_SIZE
        self.width = width
        self.widthPx = width * FIELD_SIZE
        self.screen = screen
        self.position = position

        self.grid = dict([((x, y), Field(screen, (x, y)))
                for x in range(width) for y in range(height)])

    def uncover(self, position):
        return self.grid[position].show()

    def uncoverPixels(self, position):
        return self.grid[(position[0]/FIELD_SIZE, position[1]/FIELD_SIZE)].show()

    def uncover_all(self):
        for field in self.grid.values():
            field.show()

    def display(self):
        for coords, field in self.grid.iteritems():
            field.display(self.position)

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
        if not coords in self.grid: return False

        target = self[coords]
        target.visible = True
        if target.ship is not None:
            target.ship.show(target)
            return True
        return False

    def __getitem__(self, key):
        return self.grid[key]
