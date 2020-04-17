#!/usr/bin/python3

""" TODO:
- bug: ships can sometimes not be placed
- let player choose ship locations
- AI Level unfair (50% chance of hit)
- animate sinking (blink between smoke and ship)
- pgu is annoying to use (tab breaks, enter/double click doesn't confirm)
"""

import logging
import pickle
import sys
from pathlib import Path

import pygame
from pygame.locals import *

from Board import Board
from Crosshair import Crosshair
from AI import AI
from constants import FIELD_SIZE, BG_COLOR, BOARD_WIDTH, BOARD_HEIGHT, TEXT_COLOR, MY_COLOR, \
    ENEMY_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, BASE_DIR
from generator import place_ships
from gui import Gui, load_image


class Game:

    def __init__(self):
        pygame.init()
        logo = pygame.image.load(str(BASE_DIR.joinpath('logo.png')))
        pygame.display.set_icon(logo)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("BATTLESHIPS!")
        self.clock = pygame.time.Clock()
        menu_font = pygame.font.Font('DejaVuSans.ttf', 16) # default font can't display check mark
        self.gui = Gui(self.init, self.save, self.load, self.set_ai, menu_font)
        self.font = pygame.font.Font(None, 36)

        menu_offset = (0, self.gui.menus.rect.h)
        self.my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, menu_offset)
        self.crosshair = Crosshair(self.my_board, (0, 0), menu_offset)
        self.enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, (550, 25))
        self.ai = AI(self.enemy_board)
        self.gui.update_ai_menu(self.ai.strength)

        self.textpos = pygame.Rect(10, 545, 50, 30)
        self.ship_images = {}
        for size in range(1, 6):
            self.ship_images[size] = load_image(f'ship{size}.bmp', 'gfx')

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

    def on_load(self):
        # renew display related properties
        self.my_board.on_load(self.screen)
        self.enemy_board.on_load(self.screen)
        for size in self.ship_images:
            self.ship_images[size] = load_image(f'ship{size}.bmp', 'gfx')
        self.crosshair.on_load(self.my_board)
        for ship in self.my_ships:
            ship.on_load(self.enemy_board)
        for ship in self.enemy_ships:
            ship.on_load(self.my_board)
        self.ai.board = self.enemy_board

    def save(self, dialog):
        filename = Path(dialog.value) # value defaults to current dir
        if filename.is_dir():
            filename /= 'game.sav'
        self.gui.log(f'Saving {filename}')
        state = (
            self.won,
            self.players_turn,
            self.my_board,
            self.enemy_board,
            self.my_ships,
            self.enemy_ships,
            self.remaining_ships,
            self.crosshair,
        )
        try:
            with open(filename, 'wb') as handle:
                pickle.dump(state, handle)
        except Exception as e:
            logging.exception(f'Error saving {filename}')
            self.gui.log(f'Error saving {filename}')

    def load(self, dialog):
        filename = Path(dialog.value) # value defaults to current dir
        if filename.is_dir():
            filename /= 'game.sav'
        self.gui.log(f'Loading {filename}')
        try:
            with open(filename, 'rb') as handle:
                state = pickle.load(handle)
            (
                self.won,
                self.players_turn,
                self.my_board,
                self.enemy_board,
                self.my_ships,
                self.enemy_ships,
                self.remaining_ships,
                self.crosshair,
            ) = state
            self.on_load()
        except Exception as e:
            logging.exception(f'Error loading {filename}')
            self.gui.log(f'Error loading {filename}')

    def set_ai(self, level):
        self.ai.strength = level
        self.gui.log(f'AI level set to {level.name}')
        self.gui.update_ai_menu(level)

    def switch_turns(self, value=None):
        if value is None:
            self.players_turn = not self.players_turn
        else:
            self.players_turn = value

    def log_shot(self, ship):
        who = 'You have' if self.players_turn else 'Your opponent has'
        color = MY_COLOR if self.players_turn else ENEMY_COLOR
        if ship is None:
            self.gui.log(f'{who} missed', color)
            return

        action = 'sunk' if ship.discovered else 'hit'
        whose = 'your' if ship.is_mine else 'the enemy'
        self.gui.log(f'{who} {action} {whose} ship!', color)

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
            amount = self.font.render(f'{count}x', 1, TEXT_COLOR)
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
            self.clock.tick(50)

            if self.won is None and not self.players_turn:
                hit, ship = self.ai.shoot()
                self.log_shot(ship)
                if ship is not None:
                    self.check_game_end()
                    continue
                self.switch_turns()

            for event in pygame.event.get():
                if self.gui.is_active() or self.gui.is_gui_click(event):
                    if event.type == KEYDOWN and event.key == K_ESCAPE:
                        for dialog in self.gui.dialogs:
                            if dialog.is_open():
                                dialog.close()
                        for menu in self.gui.menus._rows[0]:
                            if menu['widget'].pcls:
                                menu['widget']._close(None)
                    else:
                        # pass it on to gui
                        self.gui.handle(event)
                elif event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    # TODO: keyboard shortcuts & navigation for menu
                    if event.key == K_ESCAPE:
                        sys.exit()
                    elif event.key == K_F1:
                        self.gui.about_dlg.open()
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
                    elif event.key == K_n:
                        self.init(True)
                    elif event.key == K_s:
                        self.gui.save_dlg.open()
                    elif event.key == K_l:
                        self.gui.load_dlg.open()
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


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
