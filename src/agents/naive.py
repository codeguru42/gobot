import random
from collections.abc import Iterable

from agents.base import Agent
from agents.helpers import is_point_an_eye
from go.goboard import GameState, Move
from go.gotypes import Point


class RandomBot(Agent):
    def __init__(self, num_rows: int, num_cols: int):
        self.points = list(self._make_cache(num_rows, num_cols))

    def _make_cache(self, num_rows: int, num_cols: int) -> Iterable[Point]:
        for row in range(1, num_rows + 1):
            for col in range(1, num_cols + 1):
                yield Point(row, col)

    def select_move(self, game_state: GameState):
        random.shuffle(self.points)
        for candidate in self.points:
            play = Move.play(candidate)
            if game_state.is_valid_move(play) and not is_point_an_eye(
                game_state.board, candidate, game_state.next_player
            ):
                return play
        return Move.pass_turn()
