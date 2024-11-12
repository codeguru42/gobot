from pathlib import Path

import pytest

from go.goboard import Board
from go.gotypes import Player, Point
from tests.board.conftest import board_expected


@pytest.mark.parametrize(
    "filename,filename_expected,num_rows,num_cols,player,point",
    [
        (
            Path(__file__).parent / "data" / "board1.txt",
            Path(__file__).parent / "data" / "board1-expected.txt",
            9,
            9,
            Player.BLACK,
            Point(4, 6),
        ),
        (
            Path(__file__).parent / "data" / "board2.txt",
            Path(__file__).parent / "data" / "board2-expected.txt",
            9,
            9,
            Player.BLACK,
            Point(1, 1),
        ),
        (
            Path(__file__).parent / "data" / "board3.txt",
            Path(__file__).parent / "data" / "board3-expected.txt",
            9,
            9,
            Player.BLACK,
            Point(1, 1),
        ),
    ],
)
def test_capture(
    board: Board,
    board_expected: Board,
    filename: Path,
    filename_expected: Path,
    num_rows: int,
    num_cols: int,
    player: Player,
    point: Point,
):
    board.place_stone(player, point)
    assert board == board_expected
