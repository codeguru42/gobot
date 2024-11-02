from agents.mcts_agent import MCTSAgent
from go.goboard import Move, Board, GameState
from go.gotypes import Player, Point

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR: dict[Player, str] = {
    None: ".",
    Player.BLACK: "x",
    Player.WHITE: "o",
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
