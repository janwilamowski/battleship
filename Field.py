import pygame
from constants import FIELD_SIZE
from gui import load_image


class Field(pygame.sprite.Sprite):
    """ A game field """

    def __init__(self, screen, position, ship=None):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = position
        self.visible = False
        self.ship = ship
        if screen is not None:
            self.water = load_image('water.png', 'gfx')
            self.smoke = load_image('smoke.png', 'gfx')
            self.gray = load_image('water-gray.png', 'gfx')

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

    def display(self, offset=(0, 0)):
        if self.ship:
            if self.ship.is_mine:
                if self.visible:
                    img = self.smoke
                else:
                    img = self.image
            else: # enemy ship
                if self.ship.discovered:
                    img = self.image
                elif self.visible:
                    img = self.smoke
                else:
                    img = self.gray
        elif not self.visible:
            img = self.gray
        else:
            img = self.water

        draw_pos = img.get_rect().move(FIELD_SIZE * self.position[0] + offset[0],
                                       FIELD_SIZE * self.position[1] + offset[1])
        self.screen.blit(img, draw_pos)

    def __repr__(self):
        return f'Field {self.position}'
