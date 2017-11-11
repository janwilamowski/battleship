class AI:

    def __init__(self, strength=0):
        self.strength = 0

    def shoot(self, board):
        if self.strength is 0:
            return self.shoot_random(board)
        elif self.strength is 1:
            return self.shoot_smart(board)
        elif self.strength is 2:
            return self.shoot_unfair(board)
        else:
            return False

    def shoot_random(self, board):
        """ Picks a random field that is still invisibile. """
        return board.shoot_random()

    def shoot_smart(self, board):
        """ Tries around partial hits and avoids fields around uncovered ships. """
        return False # TODO

    def shoot_unfair(self, board):
        """ Has a 50% chance of hitting something """
        return False # TODO
