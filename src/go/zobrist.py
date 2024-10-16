import random

from go.gotypes import Player, Point

MAX63 = 0x7FFFFFFFFFFFFFFF

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in (Player.BLACK, Player.WHITE):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

HASH_CODE = table
EMPTY_BOARD = empty_board
