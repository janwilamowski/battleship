import unittest
from generator import place_ships, is_within, get_neighbors, get_opposite_direction
from Board import Board
from constants import DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.board = Board(4, 4, None)

    def test_placeShips(self):
        board = Board(10, 10, None)
        sizes = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
        ships = place_ships(board, sizes)
        for ship in ships:
            print ship

    def test_allShipsInCategoryTooLarge(self):
        board = Board(3, 3, None)
        sizes = {4: 2, 5: 1}
        ships = place_ships(board, sizes)
        assert len(ships) == 0

    def test_someShipsInCategoryTooLarge(self):
        board = Board(3, 1, None)
        sizes = {3: 2}
        ships = place_ships(board, sizes)
        print ships
        assert len(ships) == 1

    def test_isWithin(self):
        assert is_within( (1, 1), 1, 1)
        assert not is_within( (2, 1), 1, 1)
        assert not is_within( (1, 2), 1, 1)

    def test_getNeighbors(self):
        neighbors = get_neighbors( (1, 1), 2, DIR_RIGHT, self.board )
        assert len(neighbors) is 10
        assert (0, 0) in neighbors
        assert (0, 1) in neighbors
        assert (0, 2) in neighbors
        assert (1, 0) in neighbors
        assert (1, 2) in neighbors
        assert (2, 0) in neighbors
        assert (2, 2) in neighbors
        assert (3, 0) in neighbors
        assert (3, 1) in neighbors
        assert (3, 2) in neighbors

    def test_getNeighbors_corner(self):
        neighbors = get_neighbors( (0, 0), 1, DIR_RIGHT, self.board )
        assert len(neighbors) is 3
        assert (0, 1) in neighbors
        assert (1, 0) in neighbors
        assert (1, 1) in neighbors

    def test_getNeighbors_edge(self):
        neighbors = get_neighbors( (1, 0), 2, DIR_RIGHT, self.board )
        assert len(neighbors) is 6
        assert (0, 0) in neighbors
        assert (0, 1) in neighbors
        assert (1, 1) in neighbors
        assert (2, 1) in neighbors
        assert (3, 0) in neighbors
        assert (3, 1) in neighbors

    def test_getOppositeDirection(self):
        assert get_opposite_direction(DIR_RIGHT) == DIR_LEFT
        assert get_opposite_direction(DIR_LEFT) == DIR_RIGHT
        assert get_opposite_direction(DIR_UP) == DIR_DOWN
        assert get_opposite_direction(DIR_DOWN) == DIR_UP

if __name__ == '__main__':
    unittest.main()
