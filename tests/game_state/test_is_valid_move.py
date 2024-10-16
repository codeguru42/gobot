from pathlib import Path

import pytest

from gobot.goboard import GameState, Move
from gobot.gotypes import Player, Point
from test_minimax_agent import game_state


@pytest.mark.parametrize(
    "filename,num_rows,num_cols,next_player,point",
    [
        (
            Path(__file__).parent / ".." / "board" / "board1.txt",
            9,
            9,
            Player.BLACK,
            Point(4, 6),
        ),
        (
            Path(__file__).parent / ".." / "board" / "board2.txt",
            9,
            9,
            Player.BLACK,
            Point(1, 1),
        ),
        (
            Path(__file__).parent / ".." / "board" / "board3.txt",
            9,
            9,
            Player.BLACK,
            Point(1, 1),
        ),
    ],
)
def test_valid_move(
    game_state: GameState,
    filename: Path,
    num_rows: int,
    num_cols: int,
    next_player: Player,
    point: Point,
):
    assert game_state.is_valid_move(Move.play(point))
