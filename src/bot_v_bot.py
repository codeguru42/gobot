from pathlib import Path
from typing import Optional

import typer
from tensorflow.keras import models

from agents.deep_learning_agent import DeepLearningAgent
from encoders.oneplane import OnePlaneEncoder
from go.goboard import GameState
from go.gotypes import Player
from utils.print import print_board, print_move

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR: dict[Optional[Player], str] = {
    None: ".",
    Player.BLACK: "x",
    Player.WHITE: "o",
}


def main(model_path: Path):
    board_size = 19
    game = GameState.new_game(board_size)
    model = models.load_model(model_path)
    encoder = OnePlaneEncoder((board_size, board_size))
    bots = {
        Player.BLACK: DeepLearningAgent(model, encoder),
        Player.WHITE: DeepLearningAgent(model, encoder),
    }
    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
        input("Press Enter to continue...")
    print(f"{game.winner()} wins")


if __name__ == "__main__":
    typer.run(main)
