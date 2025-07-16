from pathlib import Path

import pytest

from agents.mcts_agent import MCTSAgent
from go.gotypes import Player
from utils.print import print_move


@pytest.mark.parametrize(
    "filename,num_rows,num_cols,next_player",
    ((Path(__file__).parent.parent / "data" / "board5.txt", 9, 9, Player.BLACK),),
)
def test_mcts_agent_is_play(filename, next_player, game_state):
    agent = MCTSAgent(5, 1.5)
    move = agent.select_move(game_state)
    print_move(Player.BLACK, move)
    assert move.is_play
