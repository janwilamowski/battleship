import unittest
from generator import place_ships
from Board import Board
from constants import DIR


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.board = Board(4, 4, None)

    def test_placeShips(self):
        board = Board(10, 10, None)
        sizes = {5: 1, 4: 1, 3: 2, 2: 2, 1: 3}
        ships = place_ships(board, sizes)
        for ship in ships:
            print(ship)

    def test_allShipsInCategoryTooLarge(self):
        board = Board(3, 3, None)
        sizes = {4: 2, 5: 1}
        ships = place_ships(board, sizes)
        assert len(ships) == 0

    def test_someShipsInCategoryTooLarge(self):
        board = Board(3, 1, None)
        sizes = {3: 2}
        ships = place_ships(board, sizes)
        print(ships)
        assert len(ships) == 1

if __name__ == '__main__':
    unittest.main()
