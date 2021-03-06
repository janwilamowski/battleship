import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from constants import FIELD_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from gui import load_image


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, board, position=(0, 0), offset=(0, 0)):
        super().__init__()
        self.position = position
        self.offset = offset
        self.on_load(board)

    def __getstate__(self):
        return {
            'offset': self.offset,
            'position': self.position,
        }

    def on_load(self, board):
        self.board = board
        self.image = load_image('crosshair.png', 'gfx')

    def display(self):
        pos_x = FIELD_SIZE * self.position[0] + self.offset[0]
        pos_y = FIELD_SIZE * self.position[1] + self.offset[1]
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
            print(f"ERROR: can't move towards direction {direction}")

        self.position = (self.position[0] % self.board.width, self.position[1] % self.board.height)

    def moveTo(self, position):
        pos_x = (position[0] - self.offset[0]) // FIELD_SIZE
        pos_y = (position[1] - self.offset[1]) // FIELD_SIZE
        if 0 <= pos_x < BOARD_WIDTH and 0 <= pos_y < BOARD_HEIGHT:
            self.position = (pos_x, pos_y)

    def coords(self):
        letters = 'ABCDEFGHIJ'
        return '{y}{x}'.format(y=letters[self.position[1]], x=self.position[0]+1)

    def __repr__(self):
        return f'Crosshair at {self.position}'
