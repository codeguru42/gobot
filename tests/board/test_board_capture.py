import pytest

from gobot.goboard import Board
from gobot.gotypes import Player, Point
from tests.conftest import read_board


@pytest.fixture
def board_expected(filename_expected, num_rows: int, num_cols: int):
    return read_board(filename_expected, num_rows, num_cols)


@pytest.mark.parametrize(
    "filename,filename_expected,num_rows,num_cols",
    [("board1.txt", "board1-expected.txt", 9, 9)],
)
def test_capture(
    board: Board,
    board_expected: Board,
    filename: str,
    filename_expected: str,
    num_rows: int,
    num_cols: int,
):
    board.place_stone(Player.BLACK, Point(4, 6))
    assert board == board_expected
