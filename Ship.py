import pygame
from constants import DIR_RIGHT, move_pos


class Ship(pygame.sprite.Sprite):
    def __init__(self, board, type, position=(0, 0), direction=DIR_RIGHT, is_mine=True):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.type = type
        self.fields = []
        self.is_mine = is_mine

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
            owner = self.is_mine and "my" or "enemy"
            print("hit {owner} {ship} at {pos}".format(owner=owner, ship=self, pos=field))
            self.discovered = all(f.visible for f in self.fields)
            if (self.discovered):
                print("sunk {owner} {ship}".format(owner=owner, ship=self))
        else:
            print("miss")

    def __repr__(self):
        return "Ship of type {type} in dir = {dir}, fields = {fields}".format(type=self.type, dir=self.direction, fields=self.fields)
