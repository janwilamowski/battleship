import unittest
from Board import Board
from geometry import is_within, get_neighbors, get_opposite_direction, get_diagonal_neighbors, get_orthogonal_neighbors
from constants import DIR


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.board = Board(4, 4, None)

    def test_isWithin(self):
        assert is_within( (1, 1), 1, 1)
        assert not is_within( (2, 1), 1, 1)
        assert not is_within( (1, 2), 1, 1)

    def test_getNeighbors(self):
        neighbors = get_neighbors( (1, 1), 2, DIR.RIGHT, self.board )
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
        neighbors = get_neighbors( (0, 0), 1, DIR.RIGHT, self.board )
        assert len(neighbors) is 3
        assert (0, 1) in neighbors
        assert (1, 0) in neighbors
        assert (1, 1) in neighbors

    def test_getNeighbors_edge(self):
        neighbors = get_neighbors( (1, 0), 2, DIR.RIGHT, self.board )
        assert len(neighbors) is 6
        assert (0, 0) in neighbors
        assert (0, 1) in neighbors
        assert (1, 1) in neighbors
        assert (2, 1) in neighbors
        assert (3, 0) in neighbors
        assert (3, 1) in neighbors

    def test_getDiagonalNeighbors(self):
        neighbors = get_diagonal_neighbors( (1, 1) )
        assert len(neighbors) is 4
        assert (0, 0) in neighbors
        assert (0, 2) in neighbors
        assert (2, 0) in neighbors
        assert (2, 2) in neighbors

    def test_getOrthogonalNeighbors(self):
        neighbors = get_orthogonal_neighbors( (1, 1) )
        assert len(neighbors) is 4
        assert (0, 1) in neighbors
        assert (2, 1) in neighbors
        assert (1, 0) in neighbors
        assert (1, 2) in neighbors

    def test_getOppositeDirection(self):
        assert get_opposite_direction(DIR.RIGHT) == DIR.LEFT
        assert get_opposite_direction(DIR.LEFT) == DIR.RIGHT
        assert get_opposite_direction(DIR.UP) == DIR.DOWN
        assert get_opposite_direction(DIR.DOWN) == DIR.UP

if __name__ == '__main__':
    unittest.main()
