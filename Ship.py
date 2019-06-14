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
            self.image = load_image(f'ship{size}{gray}.bmp', 'gfx')
            self.board.add_ship(self)


    def show(self, field):
        if field not in self.fields:
            return False

        self.discovered = all(f.visible for f in self.fields)
        return self.discovered


    def is_smoking(self):
        return not self.discovered and any(f.visible for f in self.fields)


    def __repr__(self):
        return f"Ship of size {self.size} in dir = {self.direction}, fields = {self.fields}"
