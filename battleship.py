#!/usr/bin/python

"""
TODO:
- game states: setup, rounds/change of control
- track status of enemy ships -> losing condition
- make visibility&status of my and their ships flexible
- randomly generate computer ships
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


def run_game():
    random.seed()
    BOARD_WIDTH, BOARD_HEIGHT = 10, 10
    SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH * FIELD_SIZE * 2 + 50, BOARD_HEIGHT * FIELD_SIZE + 200
    BG_COLOR = 150, 150, 80
    shipCountBySize = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
    won = False
    players_turn = True
    animation_running = False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("BATTLESHIPS!")
    clock = pygame.time.Clock()

    my_board = Board(BOARD_WIDTH, BOARD_HEIGHT, screen)
    crosshair = Crosshair(my_board)
    enemy_board = Board(BOARD_WIDTH, BOARD_HEIGHT, screen, (550, 0), True)
    shipsOnGrid = generate_ships(my_board, shipCountBySize)
    enemy_ships = generate_ships(enemy_board, shipCountBySize)

    font = pygame.font.Font(None, 36)
    textpos = pygame.Rect(50, 550, 50, 30)
    won_text = font.render("YOU WON!", 1, (10, 10, 10))
    won_pos = pygame.Rect(50, 600, 100, 30)

    # The main game loop
    while True:
        # win condition
        if all(ship.discovered for ship in shipsOnGrid):
            won = True

        if not players_turn:
            enemy_board.shoot_random()
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
                    my_board.uncover(crosshair.position)
                    players_turn = False
                elif event.key == K_SPACE:
                    my_board.uncover_all()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
                my_board.uncoverPixels(event.pos)
                players_turn = False
            elif event.type == MOUSEMOTION:
                crosshair.moveTo(event.pos)

        text = font.render(str(crosshair.position), 1, (10, 10, 10))

        # Redraw the background
        screen.fill(BG_COLOR)
        my_board.display()
        enemy_board.display()
        crosshair.display()
        screen.blit(text, textpos)
        if won:
            screen.blit(won_text, won_pos)

        pygame.display.flip()


def generate_ships(board, shipCountBySize):
    ships = []
    for size in sorted(shipCountBySize.keys(), reverse=True):
        amount = shipCountBySize[size]
        for i in range(amount):
            print("placing ship of size " + str(size))
            # while True:
            #     direction = random.randint(0, 3)
            #     x = random.randint(0, 9)
            #     y = random.randint(0, 9)
                # if board.ship_fits(size, (x, y), direction):
                #     break
            # ships.append(Ship(board, size, (x, y), direction))
    ships = [
            Ship(board, 5, (0,0), DIR_RIGHT),
            Ship(board, 4, (2,2), DIR_DOWN),
            Ship(board, 3, (4,2), DIR_DOWN),
            Ship(board, 3, (4,6), DIR_DOWN),
            Ship(board, 2, (9,1), DIR_LEFT),
            Ship(board, 2, (7,5), DIR_RIGHT),
            Ship(board, 1, (2,8), DIR_DOWN),
            Ship(board, 1, (9,7), DIR_LEFT),
            Ship(board, 1, (7,8), DIR_UP),
            ]
    return ships

if __name__ == "__main__":
    run_game()
