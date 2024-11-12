from pathlib import Path

import pytest

from go.goboard import Move
from go.gotypes import Player, Point


@pytest.mark.parametrize(
    "filename,num_rows,num_cols,next_player,point",
    [(Path(__file__).parent / "data" / "board4.txt", 9, 9, Player.BLACK, Point(1, 2))],
)
def test_is_valid_move(game_state, filename, num_rows, num_cols, next_player, point):
    assert game_state.is_valid_move(Move.play(point))
