import pygame
from constants import FIELD_SIZE


class Field(pygame.sprite.Sprite):
    """ A game field """

    def __init__(self, screen, position, visible=False, ship=None):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = position
        self.visible = visible
        self.smoke = ship is not None
        self.ship = ship
        if screen is not None: # TODO: use absolute path or include base
            self.image = pygame.image.load('gfx/water.png').convert_alpha()

    def show(self):
        if self.visible:
            return
        self.visible = True
        if self.ship is not None:
            self.ship.show(self)

    def hide(self):
        self.visible = False

    def display(self, offset=(0, 0)):
        if not self.visible:
            img = pygame.image.load('gfx/water-gray.png').convert_alpha()
        elif self.smoke:
            img = pygame.image.load('gfx/smoke.png').convert_alpha()
        else:
            img = self.image

        draw_pos = img.get_rect().move(FIELD_SIZE * self.position[0] + offset[0],
                                       FIELD_SIZE * self.position[1] + offset[1])
        self.screen.blit(img, draw_pos)

    def __repr__(self):
        return "Field at " + str(self.position)
