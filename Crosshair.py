import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, board, position=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.position = position
        if board is not None and board.screen is not None:
            self.image = pygame.image.load('gfx/crosshair.png').convert_alpha()

    def display(self):
        draw_pos = self.image.get_rect().move(50 * self.position[0], 50 * self.position[1])
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
        coords = (position[0] / 50, position[1] / 50)
        if coords[0] <= 9 and coords[1] <= 9:
            self.position = coords

    def __repr__(self):
        return "Crosshair at " + str(self.position)
