from pathlib import Path
import typer

from go.goboard import Board
from go.gotypes import Player, Point
from sgf import parser


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


def visit_move_node(node: parser.Node, board: Board):
    for prop in node.properties:
        match prop.ident.token:
            case "B":
                board.place_stone(Player.black, Point(prop.values[0].token))
            case "W":
                board.place_stone(Player.white, Point(prop.values[0].token))


def main(filename: Path):
    with open(filename, "r") as f:
        content = f.read()
    game = parser.parse_sgf(content)
    play(game)


if __name__ == "__main__":
    typer.run(main)
