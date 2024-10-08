import string
import time

from agents.minimax import MinimaxAgent, capture_diff
from agents.naive import RandomBot
from gobot import gotypes
from gobot.goboard import Board, Move, GameState
from gobot.gotypes import Player, Point
from gobot.zobrist import state

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR: dict[Player, str] = {
    None: ".",
    gotypes.Player.BLACK: "x",
    gotypes.Player.WHITE: "o",
}


def print_move(player: Player, move: Move):
    if move.is_pass:
        move_str = "passes"
    elif move.is_resign:
        move_str = "resigns"
    else:
        move_str = f"{COLS[move.point.col - 1]}{move.point.row}"
    print(player, move_str)


def print_board(board: Board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row, col))
            line.append(STONE_TO_CHAR[stone])
        print(f"{bump}{row} {"".join(line)}")
    print("   " + COLS[: board.num_cols])


def main():
    board_size = 9
    game = GameState.new_game(board_size)
    bots = {
        Player.BLACK: MinimaxAgent(1, capture_diff),
        Player.WHITE: MinimaxAgent(1, capture_diff),
    }
    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
    print(game.winner())


if __name__ == "__main__":
    main()
