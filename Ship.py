import pygame
from constants import DIR
from geometry import move_pos
from gui import load_image


class Ship(pygame.sprite.Sprite):
    def __init__(self, board, size, position=(0, 0), direction=DIR.RIGHT, is_mine=True):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.size = size
        self.fields = []
        self.is_mine = is_mine

        pos = position
        for i in range(size):
            self.fields.append(board[pos])
            pos = move_pos[direction](pos)

        self.direction = direction
        self.discovered = False
        if board is not None and board.screen is not None:
            gray = '-gray' if is_mine else ''
            self.image = load_image('ship{size}{gray}.bmp'.format(size=size, gray=gray), 'gfx')
            self.board.add_ship(self)

    def show(self, field):
        if field in self.fields:
            owner = self.is_mine and "my" or "enemy"
            self.discovered = all(f.visible for f in self.fields)
            if (self.discovered):
                return True
        else:
            return False

    def is_smoking(self):
        return not self.discovered and any(f.visible for f in self.fields)

    def __repr__(self):
        return "Ship of size {size} in dir = {dir}, fields = {fields}".format(size=self.size, dir=self.direction, fields=self.fields)
