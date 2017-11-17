#!/usr/bin/python

""" TODO:
- let player choose ship locations
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
from constants import FIELD_SIZE, BG_COLOR, BOARD_WIDTH, BOARD_HEIGHT, TEXT_COLOR, MY_COLOR, ENEMY_COLOR
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
        self.font = pygame.font.Font(None, 36)
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        container = gui.Container(align=-1, valign=-1)
        menus = gui.Menus([
            ('File/New', self.init, True),
            ('File/Quit', self.quit, None),
            ('AI Level/Dumb', self.set_ai, AI_Level.dumb),
            ('AI Level/Smart', self.set_ai, AI_Level.smart),
            ('Help/Help', self.open_help, None),
            ('Help/About', self.open_about, None),
            ])
        menus.rect.w, menus.rect.h = menus.resize()
        self.doc = gui.Document(width=0, height=0) # TODO: vertical?
        self.log_box = gui.ScrollArea(self.doc, SCREEN_WIDTH, 100, hscrollbar=False)
        self.log("Welcome to Battleships!")
        container.add(menus, 0, 0)
        container.add(self.log_box, 0, SCREEN_HEIGHT-100)
        self.menus = menus
        self.gui = (menus, self.log_box)
        self.app.init(container)

        menu_offset = (0, menus.rect.h)
        self.my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, menu_offset)
        self.crosshair = Crosshair(self.my_board, (0, 0), menu_offset)
        self.enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, self.screen, (550, 25))

        self.textpos = pygame.Rect(50, 550, 50, 30)

    def init(self, log):
        shipCountBySize = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
        self.won = None
        self.players_turn = True
        self.my_board.reset_fields()
        self.enemy_board.reset_fields()
        self.my_ships = place_ships(self.enemy_board, shipCountBySize)
        self.enemy_ships = place_ships(self.my_board, shipCountBySize, False)
        if log:
            self.doc.widgets = []
            self.log("Welcome to Battleships!")

    def quit(self, app):
        self.app.quit()
        sys.exit()

    def set_ai(self, level):
        self.log(level)
        self.ai.strength = level

    def open_help(self, args):
        self.log('help') # TODO

    def open_about(self, args):
        self.log('about') # TODO

    def switch_turns(self, value=None):
        if value is None:
            self.players_turn = not self.players_turn
        else:
            self.players_turn = value

    def is_gui_click(self, event):
        """ Scrolling is also clicking """
        return event.type == MOUSEBUTTONDOWN and any(gui_el.rect.collidepoint(event.pos) for gui_el in self.gui)

    def log(self, text, color=TEXT_COLOR):
        # insert on top to avoid scrolling problems
        self.doc.layout._widgets.reverse()
        self.doc.block(align=-1)
        self.doc.add(gui.Label(text, color=color))
        self.doc.layout._widgets.reverse()
        self.log_box.set_vertical_scroll(0)

    def log_shot(self, is_mine, hit, sunk):
        who = 'You have' if is_mine else 'Your opponent has'
        action = 'sunk' if sunk else 'hit'
        whose = 'the enemy' if is_mine else 'your'
        color = MY_COLOR if is_mine else ENEMY_COLOR
        if hit:
            self.log('{who} {action} {whose} ship!'.format(who=who, action=action, whose=whose), color)
        else:
            self.log('{who} missed'.format(who=who), color)

    def check_game_end(self):
        if all(ship.discovered for ship in self.my_ships):
            self.won = False
            self.log('YOU LOST!', ENEMY_COLOR)
        elif all(ship.discovered for ship in self.enemy_ships):
            self.won = True
            self.log('YOU WON!', MY_COLOR)
        # TODO: popup message?

    def show_coords(self, coords):
        self.screen.blit(coords, self.textpos)

    def run(self):
        self.init(False)

        menu_active = False

        # The main game loop
        while True:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            if not self.players_turn:
                hit, sunk = self.ai.shoot(self.enemy_board)
                self.log_shot(False, hit, sunk)
                if hit:
                    self.check_game_end()
                    continue
                self.switch_turns()

            menu_active = any(menu['widget'].pcls for menu in self.menus._rows[0])

            for event in pygame.event.get(): # TODO: suspend actions after game end
                if menu_active or self.is_gui_click(event):
                    # pass it on to pgu
                    self.app.event(event)
                elif event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    # TODO: keyboard shortcuts & navigation for menu
                    if event.key == K_ESCAPE:
                        sys.exit()
                    elif event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        self.crosshair.move(event.key)
                    elif event.key == K_RETURN:
                        hit, sunk = self.my_board.shoot(self.crosshair.position)
                        if hit is None:
                            break
                        self.log_shot(True, hit, sunk)
                        self.check_game_end()
                        self.switch_turns(hit)
                    elif event.key == K_SPACE:
                        self.my_board.uncover_all()
                        self.check_game_end()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
                    hit, sunk = self.my_board.uncoverPixels(event.pos)
                    if hit is None:
                        break
                    self.log_shot(True, hit, sunk)
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
            self.show_coords(coords)

            self.app.paint()
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
