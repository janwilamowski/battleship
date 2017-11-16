#!/usr/bin/python

""" TODO:
- let player choose ship locations
- console log of actions
- AI Level unfair (50% chance of hit)
- animate sinking (blink between smoke and ship)
- show remaining enemy ships
- use gray water for undiscovered own ships
"""

import sys
import pygame
import random
from Board import Board
from Crosshair import Crosshair
from Ship import Ship
from AI import AI
from AI import AI_Level
from pygame.locals import *
from constants import FIELD_SIZE, BG_COLOR, BOARD_WIDTH, BOARD_HEIGHT, TEXT_COLOR
from generator import place_ships
from pgu import gui


class Game:

    def __init__(self):
        random.seed()
        pygame.init()
        logo = pygame.image.load('logo.png')
        pygame.display.set_icon(logo)
        SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH * FIELD_SIZE * 2 + 50, BOARD_HEIGHT * FIELD_SIZE + 200
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("BATTLESHIPS!")
        self.clock = pygame.time.Clock()
        self.ai = AI()

        # GUI
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        container = gui.Container(align=-1, valign=-1)
        menus = gui.Menus([
            ('File/New', self.init, None),
            ('File/Quit', self.quit, None),
            ('AI Level/Dumb', self.set_ai, AI_Level.dumb),
            ('AI Level/Smart', self.set_ai, AI_Level.smart),
            ('Help/Help', self.open_help, None),
            ('Help/About', self.open_about, None),
            ])
        menus.rect.w, menus.rect.h = menus.resize()
        container.add(menus, 0, 0)
        self.menus = menus
        self.app.init(container)

        menu_offset = (0, menus.rect.h)
        self.my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, menu_offset)
        self.crosshair = Crosshair(self.my_board, (0, 0), menu_offset)
        self.enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, (550, 25))

        font = pygame.font.Font(None, 36)
        self.textpos = pygame.Rect(50, 550, 50, 30)
        self.won_text = font.render("YOU WON!", 1, TEXT_COLOR)
        self.lost_text = font.render("YOU LOST!", 1, TEXT_COLOR)
        self.font = font
        self.end_pos = pygame.Rect(50, 600, 100, 30)

    def init(self, args):
        shipCountBySize = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
        self.won = None
        self.players_turn = True
        self.my_board.reset_fields()
        self.enemy_board.reset_fields()
        self.my_ships = place_ships(self.enemy_board, shipCountBySize)
        self.enemy_ships = place_ships(self.my_board, shipCountBySize, False)

    def quit(self, app):
        self.app.quit()
        sys.exit()

    def set_ai(self, level):
        print(level)
        self.ai.strength = level

    def open_help(self, args):
        print('help') # TODO

    def open_about(self, args):
        print('about') # TODO

    def switch_turns(self):
        self.players_turn = not self.players_turn

    def is_menu_click(self, event):
        return event.type == MOUSEBUTTONDOWN and event.button == 1 and self.menus.rect.collidepoint(event.pos)

    def show_won_text(self):
        self.screen.blit(self.won_text, self.end_pos)

    def show_lost_text(self):
        self.screen.blit(self.lost_text, self.end_pos)

    def show_coords(self, coords):
        self.screen.blit(coords, self.textpos)

    def run(self):
        self.init(self)

        menu_active = False

        # The main game loop
        while True:
            # game end reached?
            if all(ship.discovered for ship in self.my_ships):
                self.won = False
            elif all(ship.discovered for ship in self.enemy_ships):
                self.won = True

            if not self.players_turn:
                if self.ai.shoot(self.enemy_board):
                    continue
                self.switch_turns()

            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            menu_active = any(menu['widget'].pcls for menu in self.menus._rows[0])

            for event in pygame.event.get(): # TODO: suspend actions after game end
                if menu_active or self.is_menu_click(event):
                    # pass it on to pgu
                    self.app.event(event)
                elif event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    elif event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        self.crosshair.move(event.key)
                    elif event.key == K_RETURN:
                        self.players_turn = self.my_board.uncover(self.crosshair.position)
                    elif event.key == K_SPACE:
                        self.my_board.uncover_all()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
                    self.players_turn = self.my_board.uncoverPixels(event.pos)
                elif event.type == MOUSEMOTION:
                    self.crosshair.moveTo(event.pos)

                coords = self.font.render(self.crosshair.coords(), 1, TEXT_COLOR)

            # Redraw the background
            self.screen.fill(BG_COLOR)
            self.my_board.display()
            self.enemy_board.display()
            self.crosshair.display()
            self.show_coords(coords)
            if self.won is True:
                self.show_won_text()
            elif self.won is False:
                self.show_lost_text()

            self.app.paint()
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
