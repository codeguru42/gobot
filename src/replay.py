from pathlib import Path

import typer

from go.goboard import Move, GameState
from go.gotypes import Player, Point
from sgf import parser, tokenizer
from sgf.tokenizer import Token
from utils.print import print_move, print_board


def play(game: parser.Collection):
    for game in visit_collection(game):
        for game_state in game:
            if game_state.last_move:
                print_move(game_state.next_player, game_state.last_move)
            print_board(game_state.board)
            print()


def visit_collection(collection: parser.Collection):
    for game in collection.games:
        yield visit_game_tree(game)


def visit_game_tree(game_tree: parser.GameTree):
    game_state = visit_root_node(game_tree.mainline.nodes[0])
    yield game_state
    yield from visit_move_nodes(game_tree.mainline.nodes[1:], game_state)


def visit_root_node(node: parser.Node) -> GameState:
    for prop in node.properties:
        match prop.ident.token:
            case "SZ":
                board_size = int(prop.values[0].token)
            case "AB":
                handicap_stones = [
                    sgf_coord_to_point(coord.token) for coord in prop.values
                ]
    return GameState.new_game(board_size, handicap_stones)


def place_stones(game_state: GameState, player: Player, coords: list[Token]):
    for coord in coords:
        if coord.token:
            point = sgf_coord_to_point(coord.token)
            game_state.board.place_stone(player, point)


def visit_move_nodes(nodes: list[parser.Node], game_state: GameState):
    for node in nodes:
        game_state = visit_move_node(node, game_state)
        yield game_state


def sgf_coord_to_move(coord: str) -> Move:
    if coord == "":
        return Move(is_pass=True)
    return Move(sgf_coord_to_point(coord))


def sgf_coord_to_point(coord):
    x = ord(coord[0]) - ord("a") + 1
    y = ord(coord[1]) - ord("a") + 1
    point = Point(x, y)
    return point


class InvalidPlayerException(Exception):
    def __init__(self, message):
        super().__init__(message)


def visit_move_node(node: parser.Node, game_state: GameState) -> GameState:
    prop = node.properties[0]
    move = sgf_coord_to_move(prop.values[0].token)
    match prop.ident.token:
        case "B":
            player = Player.BLACK
        case "W":
            player = Player.WHITE
        case _:
            raise InvalidPlayerException(
                f"Invalid player: {prop.ident.token}"
            )
    assert game_state.next_player == player
    game_state = game_state.apply_move(move)
    return game_state


def main(filename: Path):
    with open(filename, "r") as f:
        content = f.read()
    tokens = tokenizer.tokens(content)
    game = parser.parse_sgf(tokens)
    play(game)


if __name__ == "__main__":
    typer.run(main)
