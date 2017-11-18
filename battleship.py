#!/usr/bin/python

""" TODO:
- let player choose ship locations
- AI Level unfair (50% chance of hit)
- animate sinking (blink between smoke and ship)
"""

import sys
import pygame
from Board import Board
from Crosshair import Crosshair
from Ship import Ship
from AI import AI
from pygame.locals import *
from constants import FIELD_SIZE, BG_COLOR, BOARD_WIDTH, BOARD_HEIGHT, TEXT_COLOR, MY_COLOR, \
    ENEMY_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT
from generator import place_ships
from gui import Gui


class Game:

    def __init__(self):
        pygame.init()
        logo = pygame.image.load('logo.png')
        pygame.display.set_icon(logo)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("BATTLESHIPS!")
        self.clock = pygame.time.Clock()
        self.ai = AI()
        self.gui = Gui(self.init, self.set_ai)
        self.font = pygame.font.Font(None, 36)

        menu_offset = (0, self.gui.menus.rect.h)
        self.my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, menu_offset)
        self.crosshair = Crosshair(self.my_board, (0, 0), menu_offset)
        self.enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, (550, 25))

        self.textpos = pygame.Rect(10, 545, 50, 30)
        self.ship_images = {}
        for size in range(1, 6):
            image = pygame.image.load('gfx/ship{size}.bmp'.format(size=size)).convert_alpha()
            self.ship_images[size] = image

    def init(self, log):
        shipCountBySize = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
        self.won = None
        self.players_turn = True
        self.my_board.reset_fields()
        self.enemy_board.reset_fields()
        self.my_ships = place_ships(self.enemy_board, shipCountBySize)
        self.enemy_ships = place_ships(self.my_board, shipCountBySize, False)
        self.remaining_ships = shipCountBySize
        if log:
            self.gui.clear_log()
            self.gui.log("Welcome to Battleships!")

    def set_ai(self, level):
        self.ai.strength = level
        self.gui.log('AI level set to {l}'.format(l=level.name))

    def switch_turns(self, value=None):
        if value is None:
            self.players_turn = not self.players_turn
        else:
            self.players_turn = value

    def log_shot(self, ship):
        who = 'You have' if self.players_turn else 'Your opponent has'
        color = MY_COLOR if self.players_turn else ENEMY_COLOR
        if ship is None:
            self.gui.log('{who} missed'.format(who=who), color)
            return

        action = 'sunk' if ship.discovered else 'hit'
        whose = 'your' if ship.is_mine else 'the enemy'
        self.gui.log('{who} {action} {whose} ship!'.format(who=who, action=action, whose=whose), color)

        if ship.discovered and not ship.is_mine:
            self.remaining_ships[ship.size] -= 1

    def check_game_end(self):
        if self.won is not None: return

        if all(ship.discovered for ship in self.my_ships):
            self.won = False
            self.gui.log('YOU LOST!', ENEMY_COLOR)
        elif all(ship.discovered for ship in self.enemy_ships):
            self.won = True
            self.gui.log('YOU WON!', MY_COLOR)
        # TODO: popup message?

    def show_remaining_ships(self):
        offset = 60
        for size, count in self.remaining_ships.items():
            text_pos = pygame.Rect(offset, 545, 50, 30)
            amount = self.font.render('{c}x'.format(c=count), 1, TEXT_COLOR)
            self.screen.blit(amount, text_pos)
            offset += 30

            ship_size = size * FIELD_SIZE
            ship_pos = pygame.Rect(offset, 535, ship_size, FIELD_SIZE)
            image = self.ship_images[size]
            self.screen.blit(image, ship_pos)
            offset += ship_size + 20

    def show_coords(self, coords):
        self.screen.blit(coords, self.textpos)

    def run(self):
        self.init(False)

        # The main game loop
        while True:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            if self.won is None and not self.players_turn:
                hit, ship = self.ai.shoot(self.enemy_board)
                self.log_shot(ship)
                if ship is not None:
                    self.check_game_end()
                    continue
                self.switch_turns()

            for event in pygame.event.get():
                if self.gui.is_active() or self.gui.is_gui_click(event):
                    # pass it on to gui
                    self.gui.handle(event)
                elif event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    # TODO: keyboard shortcuts & navigation for menu
                    if event.key == K_ESCAPE:
                        sys.exit()
                    elif event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        self.crosshair.move(event.key)
                    elif event.key == K_RETURN and self.won is None:
                        hit, ship = self.my_board.shoot(self.crosshair.position)
                        if hit is None:
                            break
                        self.log_shot(ship)
                        self.check_game_end()
                        self.switch_turns(hit)
                    elif event.key == K_SPACE:
                        self.my_board.uncover_all()
                        self.check_game_end()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.won is None:  # left click
                    hit, ship = self.my_board.uncoverPixels(event.pos)
                    if hit is None:
                        break
                    self.log_shot(ship)
                    self.check_game_end()
                    self.switch_turns(hit)
                elif event.type == MOUSEMOTION:
                    self.crosshair.moveTo(event.pos)

                coords = self.font.render(self.crosshair.coords(), 1, TEXT_COLOR)

            # Redraw the background
            self.screen.fill(BG_COLOR)
            self.my_board.display()
            self.enemy_board.display()
            self.crosshair.display()
            self.show_remaining_ships()
            self.show_coords(coords)

            self.gui.paint()
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
