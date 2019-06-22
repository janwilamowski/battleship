from enum import Enum, auto
import random
from geometry import get_diagonal_neighbors, get_orthogonal_neighbors, get_neighbors_ship


class AI_Level(Enum):
    dumb, smart = [auto() for _ in range(2)]


class AI:

    def __init__(self, board, strength=AI_Level.smart):
        self.board = board
        self.strength = strength

    def shoot(self):
        """ Shoots at the given board, depending on the current AI level.
            Returns True if a ship was hit and False otherwise.
        """
        strategies = {
            AI_Level.dumb: self.shoot_random,
            AI_Level.smart: self.shoot_smart,
        }
        return strategies[self.strength]()

    def shoot_random(self):
        """ Picks a random field that is still invisibile. """
        return self.board.shoot_random()

    def shoot_smart(self):
        """ Tries around partial hits and avoids fields around uncovered ships. """
        partial_hits = [field for field in self.board.grid.values() \
            if field.ship and field.ship.is_smoking() and field.visible]
        diagonal_neighbors = set(dn \
            for field in partial_hits \
            for dn in get_diagonal_neighbors(field.position) )
        orthogonal_neighbors = set(on \
            for field in partial_hits \
            for on in get_orthogonal_neighbors(field.position) )
        potential_neighbors = orthogonal_neighbors.difference(diagonal_neighbors)
        neighbors = [coords for coords in potential_neighbors \
            if coords in self.board.grid and not self.board.grid[coords].visible]
        if neighbors:
            return self.board.shoot(random.choice(neighbors))

        # exclude fields around uncovered ships
        uncovered_ships = set(field.ship \
            for field in self.board.grid.values() \
            if field.ship and field.ship.discovered )
        ship_neighbors = set(n \
            for ship in uncovered_ships \
            for n in get_neighbors_ship(ship, self.board))
        targets = set(field.position \
            for field in self.board.grid.values() \
            if not field.visible ).difference(ship_neighbors)
        return self.board.shoot( random.choice(list(targets)) )
