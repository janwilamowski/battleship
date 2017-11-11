#!/usr/bin/python

""" TODO:
- let player choose ship locations
- menu screen
- console log of actions
- AI Levels dumb (random), smart (around previous hits) and unfair (50% chance of hit)
- animate sinking (blink between smoke and ship)
"""

import sys
import pygame
import random
from Board import Board
from Crosshair import Crosshair
from Ship import Ship
from pygame.locals import *
from constants import DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT, FIELD_SIZE
from generator import place_ships


def run_game():
    random.seed()
    BOARD_WIDTH, BOARD_HEIGHT = 10, 10
    SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH * FIELD_SIZE * 2 + 50, BOARD_HEIGHT * FIELD_SIZE + 200
    BG_COLOR = 150, 150, 80
    shipCountBySize = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
    won = None
    players_turn = True
    animation_running = False

    pygame.init()
    logo = pygame.image.load('logo.png')
    pygame.display.set_icon(logo)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("BATTLESHIPS!")
    clock = pygame.time.Clock()

    my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, screen)
    crosshair = Crosshair(my_board)
    enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, screen, (550, 0))
    my_ships = place_ships(enemy_board, shipCountBySize)
    enemy_ships = place_ships(my_board, shipCountBySize, False)

    font = pygame.font.Font(None, 36)
    textpos = pygame.Rect(50, 550, 50, 30)
    won_text = font.render("YOU WON!", 1, (10, 10, 10))
    lost_text = font.render("YOU LOST!", 1, (10, 10, 10))
    end_pos = pygame.Rect(50, 600, 100, 30)

    # The main game loop
    while True:
        # game end reached?
        if all(ship.discovered for ship in my_ships):
            won = False
        elif all(ship.discovered for ship in enemy_ships):
            won = True

        if not players_turn:
            if enemy_board.shoot_random():
                continue
            players_turn = not players_turn

        # Limit frame speed to 50 FPS
        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    crosshair.move(event.key)
                elif event.key == K_RETURN:
                    players_turn = my_board.uncover(crosshair.position)
                elif event.key == K_SPACE:
                    my_board.uncover_all()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
                players_turn = my_board.uncoverPixels(event.pos)
            elif event.type == MOUSEMOTION:
                crosshair.moveTo(event.pos)

        text = font.render(str(crosshair.position), 1, (10, 10, 10))

        # Redraw the background
        screen.fill(BG_COLOR)
        my_board.display()
        enemy_board.display()
        crosshair.display()
        screen.blit(text, textpos)
        if won is True:
            screen.blit(won_text, end_pos)
        elif won is False:
            screen.blit(lost_text, end_pos)

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
