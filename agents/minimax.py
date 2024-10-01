from enum import Enum
import random

from agents.base import Agent
from gobot.goboard import GameState


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


def best_result(game_state: GameState):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.WIN
        elif game_state.winner() is None:
            return GameResult.DRAW
        else:
            return GameResult.LOSS

    best_result_so_far = GameResult.LOSS
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state)
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    return best_result_so_far


def reverse_game_result(game_result: GameResult):
    match game_result:
        case GameResult.WIN:
            return GameResult.LOSS
        case GameResult.DRAW:
            return GameResult.DRAW
        case GameResult.LOSS:
            return GameResult.WIN
