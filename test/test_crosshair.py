import unittest
from Board import Board
from Crosshair import Crosshair
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT


class CrosshairTest(unittest.TestCase):
    def test_move(self):
        board = Board(4, 5, None)
        crosshair = Crosshair(board)
        assert (0, 0) == crosshair.position
        crosshair.move(K_DOWN)
        assert (0, 1) == crosshair.position
        crosshair.move(K_RIGHT)
        assert (1, 1) == crosshair.position
        crosshair.move(K_UP)
        assert (1, 0) == crosshair.position
        crosshair.move(K_LEFT)
        assert (0, 0) == crosshair.position
        crosshair.move(K_UP)
        assert (0, 4) == crosshair.position
        crosshair.move(K_LEFT)
        assert (3, 4) == crosshair.position

if __name__ == "__main__":
    unittest.main()
