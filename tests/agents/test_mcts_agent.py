from pathlib import Path

import pytest

from agents.mcts_agent import MCTSAgent
from go.goboard import GameState
from go.gotypes import Player
from utils.print import print_move


@pytest.mark.parametrize(
    "filename_board,num_rows,num_cols,next_player",
    ((Path(__file__).parent.parent / "data" / "board5.txt", 9, 9, Player.BLACK),),
)
def test_mcts_agent_is_play(
    filename_board: Path, next_player: Player, game_state: GameState
):
    agent = MCTSAgent(5, 1.5)
    move = agent.select_move(game_state)
    print_move(Player.BLACK, move)
    assert move.is_play
