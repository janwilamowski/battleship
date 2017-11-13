from enum import Enum
import random
from generator import get_diagonal_neighbors, get_orthogonal_neighbors, get_neighbors_ship


class AI_Level(Enum):
    dumb, smart, unfair = range(3)


class AI:

    def __init__(self, strength=AI_Level.smart):
        self.strength = strength

    def shoot(self, board):
        """ Shoots at the given board, depending on the current AI level.
            Returns True if a ship was hit and False otherwise.
        """
        if self.strength is AI_Level.dumb:
            return self.shoot_random(board)
        elif self.strength is AI_Level.smart:
            return self.shoot_smart(board)
        elif self.strength is AI_Level.unfair:
            return self.shoot_unfair(board)
        else:
            return False

    def shoot_random(self, board):
        """ Picks a random field that is still invisibile. """
        return board.shoot_random()

    def shoot_smart(self, board):
        """ Tries around partial hits and avoids fields around uncovered ships. """
        partial_hits = [field for field in board.grid.values() \
            if field.ship and field.ship.is_smoking() and field.visible]
        diagonal_neighbors = set( dn \
            for field in partial_hits \
            for dn in get_diagonal_neighbors(field.position) )
        orthogonal_neighbors = set( on \
            for field in partial_hits \
            for on in get_orthogonal_neighbors(field.position) )
        potential_neighbors = orthogonal_neighbors.difference(diagonal_neighbors)
        neighbors = [coords for coords in potential_neighbors \
            if coords in board.grid and not board.grid[coords].visible]
        if len(neighbors) > 0:
            return board.shoot(random.choice(neighbors))

        # exclude fields around uncovered ships
        uncovered_ships = set( field.ship \
            for field in board.grid.values() \
            if field.ship and field.ship.discovered )
        ship_neighbors = set( n \
            for ship in uncovered_ships \
            for n in get_neighbors_ship(ship, board))
        targets = set( field.position \
            for field in board.grid.values() \
            if not field.visible ).difference(ship_neighbors)
        return board.shoot( random.choice(list(targets)) )

    def shoot_unfair(self, board):
        """ Has a 50% chance of hitting something """
        return self.shoot_random(board) # TODO - may not be needed
