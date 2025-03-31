from typing import Optional

from agents.mcts_agent import MCTSAgent
from go.goboard import GameState
from go.gotypes import Player
from utils.print import print_board, print_move

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR: dict[Optional[Player], str] = {
    None: ".",
    Player.BLACK: "x",
    Player.WHITE: "o",
}


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    num_rounds = 5
    temperature = 1.5
    bots = {
        Player.BLACK: MCTSAgent(num_rounds, temperature),
        Player.WHITE: MCTSAgent(num_rounds, temperature),
    }
    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
    print(f"{game.winner()} wins")


if __name__ == "__main__":
    main()
