import pytest

from agents.minimax import MinimaxAgent, capture_diff
from gobot.goboard import Board, GameState, Move
from gobot.gotypes import Player, Point
from tests.conftest import board


@pytest.fixture
def game_state(board: Board, next_player: Player) -> GameState:
    return GameState(board, next_player)


@pytest.fixture
def minimax_agent() -> MinimaxAgent:
    return MinimaxAgent(1, capture_diff)


@pytest.mark.parametrize(
    "filename,num_rows,num_cols,next_player", [("board1.txt", 9, 9, Player.BLACK)]
)
def test_board1(
    filename: str,
    num_rows: int,
    num_cols: int,
    next_player: Player,
    minimax_agent: MinimaxAgent,
    game_state: GameState,
):
    assert minimax_agent.select_move(game_state) == Move.pass_turn()


@pytest.mark.parametrize(
    "filename,num_rows,num_cols,next_player", [("board2.txt", 9, 9, Player.WHITE)]
)
def test_board2(
    filename: str,
    num_rows: int,
    num_cols: int,
    next_player: Player,
    minimax_agent: MinimaxAgent,
    game_state: GameState,
):
    assert minimax_agent.select_move(game_state) == Move.play(Point(2, 3))
