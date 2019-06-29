import pygame
from constants import DIR
from geometry import move_pos
from gui import load_image


class Ship(pygame.sprite.Sprite):
    def __init__(self, board, size, position=(0, 0), direction=DIR.RIGHT, is_mine=True):
        super().__init__()
        self.board = board
        self.size = size
        self.fields = []
        self.is_mine = is_mine

        pos = position
        for _ in range(size):
            self.fields.append(board[pos])
            pos = move_pos[direction](pos)

        self.direction = direction
        self.discovered = False
        self.on_load()

    def __getstate__(self):
        return {
            'discovered': self.discovered,
            'board': self.board,
            'size': self.size,
            'is_mine': self.is_mine,
            'fields': self.fields,
            'direction': self.direction,
        }

    def on_load(self, board=None):
        if board:
            self.board = board
        gray = '-gray' if self.is_mine else ''
        self.image = load_image(f'ship{self.size}{gray}.bmp', 'gfx')
        self.board.add_ship(self)

    def show(self, field):
        if field not in self.fields:
            return False

        self.discovered = all(f.visible for f in self.fields)
        return self.discovered

    def is_smoking(self):
        return not self.discovered and any(f.visible for f in self.fields)

    def __repr__(self):
        return f"Ship of size {self.size} in dir = {self.direction}, fields = {self.fields}, {'mine' if self.is_mine else 'enemy'}, disc={self.discovered}"
