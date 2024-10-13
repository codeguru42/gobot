import pytest

from gobot.goboard import Board
from gobot.gotypes import Player, Point


@pytest.fixture
def board(filename: str, num_rows: int, num_cols: int) -> Board:
    return read_board(filename, num_cols, num_rows)


def read_board(filename, num_cols, num_rows):
    b = Board(num_rows, num_cols)
    with open(filename, "r") as f:
        for r, line in enumerate(f, start=1):
            for c, stone in enumerate(line, start=1):
                match stone:
                    case "x":
                        b.place_stone(Player.BLACK, Point(r, c))
                    case "o":
                        b.place_stone(Player.WHITE, Point(r, c))
                    case ".":
                        pass
    return b