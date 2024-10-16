import random
from collections.abc import Callable
from enum import Enum

from agents.base import Agent
from go.goboard import GameState, Move
from go.gotypes import Player, Point

MAX_SCORE = 999999
MIN_SCORE = -999999


class GameResult(Enum):
    LOSS = 1
    DRAW = 2
    WIN = 3


class MinimaxAgent(Agent):
    def __init__(self, max_depth: int, eval_fn: Callable[[GameState], int]):
        super().__init__()
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state: GameState) -> Move:
        best_moves = []
        best_score = None

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(
                next_state, self.max_depth, MIN_SCORE, MAX_SCORE, self.eval_fn
            )
            our_best_outcome = -opponent_best_outcome
            if not best_moves or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)


def best_result(
    game_state: GameState,
    max_depth: int,
    best_black: int,
    best_white: int,
    eval_fn: Callable[[GameState], int],
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
        opponent_best_result = best_result(
            next_state, max_depth - 1, best_black, best_white, eval_fn
        )
        our_result = -opponent_best_result
        if our_result > best_result_so_far:
            best_result_so_far = our_result
        if game_state.next_player == Player.WHITE:
            if best_result_so_far > best_white:
                best_white = best_result_so_far
            outcome_for_black = -best_result_so_far
            if outcome_for_black < best_black:
                return best_result_so_far
        elif game_state.next_player == Player.BLACK:
            if best_result_so_far > best_black:
                best_black = best_result_so_far
            outcome_for_white = -best_result_so_far
            if outcome_for_white < best_white:
                return best_result_so_far
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
