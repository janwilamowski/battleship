import pygame
from constants import DIR_RIGHT, move_pos


class Ship(pygame.sprite.Sprite):
    def __init__(self, board, type, position=(0, 0), direction=DIR_RIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.type = type
        self.fields = []

        pos = position
        for i in range(type):
            self.fields.append(board[pos])
            pos = move_pos[direction](pos)

        self.direction = direction
        self.discovered = False
        if board is not None and board.screen is not None:
            self.image = pygame.image.load('gfx/ship{type}.bmp'.format(type=type)).convert_alpha()
            self.board.add_ship(self)

    def show(self, field):
        if field in self.fields:
            print("hit {ship} at {pos}".format(ship=self, pos=field))
            self.discovered = all(f.visible for f in self.fields)
            if (self.discovered):
                print("sunk {ship}".format(ship=self))
                for field in self.fields: # TODO: use event
                    field.smoke = False
        else:
            print("miss")

    def __repr__(self):
        return "Ship of type {type} in dir = {dir}, fields = {fields}".format(type=self.type, dir=self.direction, fields=self.fields)
