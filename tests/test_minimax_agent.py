import pytest

from agents.minimax import MinimaxAgent, capture_diff
from gobot.goboard import Board, GameState, Move
from gobot.gotypes import Player, Point


@pytest.fixture
def board(filename: str, num_rows: int, num_cols: int) -> Board:
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
