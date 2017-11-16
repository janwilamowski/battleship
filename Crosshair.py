import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, board, position=(0, 0), offset=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.position = position
        self.offset = offset
        if board is not None and board.screen is not None:
            self.image = pygame.image.load('gfx/crosshair.png').convert_alpha()

    def display(self):
        pos_x = 50 * self.position[0] + self.offset[0]
        pos_y = 50 * self.position[1] + self.offset[1]
        draw_pos = self.image.get_rect().move(pos_x, pos_y)
        self.board.screen.blit(self.image, draw_pos)

    def move(self, direction):
        if direction == K_UP:
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == K_DOWN:
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == K_RIGHT:
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == K_LEFT:
            self.position = (self.position[0] - 1, self.position[1])
        else:
            print("ERROR: can't move towards direction " + direction)

        self.position = (self.position[0] % self.board.width, self.position[1] % self.board.height)

    def moveTo(self, position):
        pos_x = (position[0] - self.offset[0]) / 50
        pos_y = (position[1] - self.offset[1]) / 50
        if 0 <= pos_x <= 9 and 0 <= pos_y <= 9:
            self.position = (pos_x, pos_y)

    def coords(self):
        letters = 'ABCDEFGHIJ'
        return '{x}{y}'.format(x=letters[self.position[0]], y=self.position[1]+1)

    def __repr__(self):
        return "Crosshair at " + str(self.position)
