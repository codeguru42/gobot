from pathlib import Path

import pytest

from go.goboard import Board, GameState
from go.gotypes import Player, Point


@pytest.fixture
def game_state(board: Board, next_player: Player) -> GameState:
    return GameState(board, next_player)


@pytest.fixture
def board(filename_board: str | Path, num_rows: int, num_cols: int) -> Board:
    return read_board(filename_board, num_cols, num_rows)


def read_board(filename: str | Path, num_cols: int, num_rows: int):
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
