from typing import Optional
from go.goboard import Board, Move
from go.gotypes import Player, Point

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR: dict[Optional[Player], str] = {
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
        print(f"{bump}{row} {"".join(f" {p} " for p in line)}")
    print("   " + COLS[: board.num_cols])
