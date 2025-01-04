import numpy as np

from agents.mcts_agent import MCTSAgent
from bot_v_bot import print_board, print_move
from encoders.base import get_encoder_by_name
from go.goboard import GameState


def generate_game(
    board_size: tuple[int, int], rounds: int, max_moves: int, temperature: float
):
    boards, moves = [], []
    encoder = get_encoder_by_name("oneplane", board_size)
    game = GameState.new_game(board_size)
    bot = MCTSAgent(rounds, temperature)
    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game)
        if move.is_play:
            boards.append(encoder.encode(game))
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)

        print_move(game.next_player, move)
        game = game.apply_move(move)
        num_moves += 1
        if num_moves >= max_moves:
            break
    return np.array(boards), np.array(moves)
