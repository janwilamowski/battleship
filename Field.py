import pygame
from constants import FIELD_SIZE
from gui import load_image


class Field(pygame.sprite.Sprite):
    """ A game field """

    water = smoke = gray = None

    def __init__(self, screen, position):
        super().__init__()

        self.position = position
        self.visible = False
        self.on_load(screen)
        self.ship = None

    def __getstate__(self):
        return {
            'visible': self.visible,
            'position': self.position,
            'ship': self.ship,
        }

    def on_load(self, screen):
        self.screen = screen
        if not Field.water:
            Field.water = load_image('water.png', 'gfx')
        if not Field.smoke:
            Field.smoke = load_image('smoke.png', 'gfx')
        if not Field.gray:
            Field.gray = load_image('water-gray.png', 'gfx')

    def show(self):
        """ Uncovers this field and returns true if a ship was hit """
        if self.visible:
            return None
        self.visible = True
        if self.ship is None:
            return False
        self.ship.show(self)
        return True

    def hide(self):
        self.visible = False

    def set_ship(self, ship, image):
        self.ship = ship
        self.image = image

    def display(self, offset=(0, 0)):
        img = None
        if self.ship:
            if self.ship.is_mine:
                if self.visible:
                    img = Field.smoke
                else:
                    img = self.image
            else: # enemy ship
                if self.ship.discovered:
                    img = self.image
                elif self.visible:
                    img = Field.smoke
                else:
                    img = Field.gray
        elif not self.visible:
            img = Field.gray
        else:
            img = Field.water

        if not img:
            print('no image for', self)
            return

        draw_pos = img.get_rect().move(FIELD_SIZE * self.position[0] + offset[0],
                                       FIELD_SIZE * self.position[1] + offset[1])
        self.screen.blit(img, draw_pos)

    def __repr__(self):
        return f'Field {self.position} {self.visible}'
