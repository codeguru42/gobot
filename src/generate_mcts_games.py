import numpy as np
import typer
from typing_extensions import Annotated

from agents.mcts_agent import MCTSAgent
from bot_v_bot import print_board, print_move
from encoders.base import get_encoder_by_name
from go.goboard import GameState


def generate_game(board_size: int, rounds: int, max_moves: int, temperature: float):
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


def main(
    board_out: str,
    move_out: str,
    board_size: Annotated[int, typer.Option("-b")] = 9,
    rounds: Annotated[int, typer.Option("-r")] = 1000,
    temperature: Annotated[float, typer.Option("-t")] = 0.8,
    max_moves: Annotated[int, typer.Option("-m")] = 60,
    num_games: Annotated[int, typer.Option("-n")] = 10,
):
    xs = []
    ys = []

    for i in range(num_games):
        print(f"Generating game {i+1}/{num_games}")
        x, y = generate_game(board_size, rounds, max_moves, temperature)
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)
    y = np.concatenate(ys)
    np.save(board_out, x)
    np.save(move_out, y)


if __name__ == "__main__":
    typer.run(main)
