from enum import Enum
import module_locator

BASE_DIR = module_locator.module_path()

BG_COLOR = 150, 150, 80
TEXT_COLOR = 10, 10, 10
MY_COLOR = 0, 0, 200
ENEMY_COLOR = 200, 0, 0

FIELD_SIZE = 50
BOARD_WIDTH, BOARD_HEIGHT = 10, 10
SCREEN_WIDTH = BOARD_WIDTH * FIELD_SIZE * 2 + 50
SCREEN_HEIGHT = BOARD_HEIGHT * FIELD_SIZE + 200

class DIR(Enum):
    """ Direction of ships and movements. Values represent angles in degrees. """
    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270
