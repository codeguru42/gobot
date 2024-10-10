from collections.abc import Callable
from enum import Enum
import random

from agents.base import Agent
from gobot.goboard import GameState
from gobot.gotypes import Point, Player


MAX_SCORE = 999999
MIN_SCORE = -999999


class GameResult(Enum):
    LOSS = 1
    DRAW = 2
    WIN = 3


class MinimaxAgent(Agent):
    def select_move(self, game_state: GameState):
        winning_moves = []
        draw_moves = []
        losing_moves = []

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state)
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            if our_best_outcome == GameResult.WIN:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.DRAW:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)

        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)


def best_result(
    self, game_state: GameState, max_depth: int, eval_fn: Callable[[GameState], int]
) -> int:
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:
        return eval_fn(game_state)

    best_result_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        our_result = -opponent_best_result
        if our_result > best_result_so_far:
            best_result_so_far = our_result
    return best_result_so_far


def capture_diff(game_state: GameState) -> int:
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = Point(r, c)
            color = game_state.board.get(p)
            match color:
                case Player.BLACK:
                    black_stones += 1
                case Player.WHITE:
                    white_stones += 1
    diff = black_stones - white_stones
    if game_state.next_player == Player.BLACK:
        return diff
    return -diff
