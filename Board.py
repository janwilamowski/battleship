import random
import pygame
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
        pos_x = (position[0] - self.offset[0]) // FIELD_SIZE
        pos_y = (position[1] - self.offset[1]) // FIELD_SIZE
        if 0 <= pos_x < BOARD_WIDTH and 0 <= pos_y < BOARD_HEIGHT:
            return self.shoot((pos_x, pos_y))
        else:
            return None, None # ignore

    def uncover_all(self):
        for field in self.grid.values():
            field.show()

    def reset_fields(self):
        self.grid = dict(((x, y), Field(self.screen, (x, y)))
                for x in range(self.width) for y in range(self.height))

    def display(self):
        for field in self.grid.values():
            field.display(self.offset)

    def __getstate__(self):
        return {
            'width': self.width,
            'height': self.height,
            'heightPx': self.heightPx,
            'widthPx': self.widthPx,
            'grid': self.grid,
            'offset': self.offset,
        }

    def on_load(self, screen):
        self.screen = screen
        for field in self.grid.values():
            field.on_load(screen)

    def add_ship(self, ship):
        if not self.screen: return
        offset = 0
        for field in ship.fields:
            pos = field.position
            if pos not in self.grid:
                print(f"field {pos} isn't in this board")
                continue
            rect = pygame.Rect(offset, 0, FIELD_SIZE, FIELD_SIZE)
            surface = pygame.Surface(rect.size).convert(self.screen)
            surface.blit(ship.image, (0, 0), rect)
            img = pygame.transform.rotate(surface, ship.direction.value)
            self[pos].set_ship(ship, img)
            offset += FIELD_SIZE

    def shoot_random(self):
        targets = [pos for pos in self.grid if not self[pos].visible]
        return self.shoot(random.choice(targets))

    def shoot(self, coords):
        """ Uncovers the field at the given coordinates.
            Returns True if a ship was hit and False otherwise. Updates the ship if it was hit.
        """
        if not coords in self.grid or self.grid[coords].visible: return None, None

        target = self[coords]
        target.visible = True
        if target.ship:
            target.ship.show(target)
            return True, target.ship
        return False, None

    def __getitem__(self, key):
        return self.grid[key]
