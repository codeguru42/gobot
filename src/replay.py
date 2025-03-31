from pathlib import Path

import typer

from go.goboard import Board, Move
from go.gotypes import Player, Point
from sgf import parser, tokenizer
from utils.print import print_move, print_board

def play(game: parser.Collection):
    visit_collection(game)


def visit_collection(collection: parser.Collection):
    for game in collection.games:
        visit_game_tree(game)


def visit_game_tree(game: parser.GameTree):
    board = visit_root_node(game.mainline.nodes[0])
    visit_move_nodes(game.mainline.nodes[1:], board)


def visit_root_node(node: parser.Node):
    for prop in node.properties:
        match prop.ident.token:
            case "SZ":
                board_size = int(prop.values[0].token)
    board = Board(board_size, board_size)
    return board


def visit_move_nodes(nodes: list[parser.Node], board: Board):
    for node in nodes:
        visit_move_node(node, board)

def sgf_coord_to_point(coord: str) -> Point:
    x = ord(coord[0]) - ord("a")
    y = ord(coord[1]) - ord("a")
    return Point(x, y)


class InvalidPlayerException(Exception):
    def __init__(self, message):
        super().__init__(message)


def visit_move_node(node: parser.Node, board: Board):
    prop = node.properties[0]
    point = sgf_coord_to_point(prop.values[0].token)
    match prop.ident.token:
        case "B":
            player = Player.BLACK
        case "W":
            player = Player.WHITE
        case _:
            raise InvalidPlayerException(f"Invalid player: {prop.ident.token}") # This can happen if the move is not valid (e.g., pass or resign)
    board.place_stone(player, point)
    print_move(player, Move(point))
    print_board(board)
    print()


def main(filename: Path):
    with open(filename, "r") as f:
        content = f.read()
    tokens = tokenizer.tokens(content)
    game = parser.parse_sgf(tokens)
    play(game)


if __name__ == "__main__":
    typer.run(main)
