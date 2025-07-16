from pathlib import Path

import pytest

from agents.helpers import is_point_an_eye
from go.goboard import Board
from go.gotypes import Point, Player


@pytest.mark.parametrize(
    "filename_board,num_rows,num_cols,point,color,expected",
    [
        (
            Path(__file__).parent.parent / "data" / "board-eyes.txt",
            9,
            9,
            Point(row=4, col=5),
            Player.BLACK,
            True,
        )
    ],
)
def test_is_point_an_eye(
    filename_board: Path,
    num_rows,
    num_cols,
    board: Board,
    point: Point,
    color: Player,
    expected: bool,
) -> None:
    assert is_point_an_eye(board, point, color) == expected
