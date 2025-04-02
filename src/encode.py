import tarfile
from io import BufferedReader
from pathlib import Path
from typing import Iterable

import typer

from go.goboard import GameState
from replay import visit_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens
from utils.print import print_move, print_board


def extract_files(input_directory: Path) -> Iterable[BufferedReader]:
    for file in input_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def parse_files(sgf_files: Iterable[BufferedReader]) -> Iterable[Collection]:
    for f in sgf_files:
        content = f.read().decode("utf-8")
        yield parse_sgf(tokens(content))


def replay_games(
    collections: Iterable[Collection],
) -> Iterable[Iterable[Iterable[GameState]]]:
    for collection in collections:
        yield visit_collection(collection)


def main(input_directory: Path, output_directory: Path):
    sgf_files = extract_files(input_directory)
    collections = parse_files(sgf_files)
    for games in replay_games(collections):
        for game in games:
            for game_state in game:
                if game_state.last_move:
                    print_move(
                        game_state.previous_state.next_player, game_state.last_move
                    )
                print_board(game_state.board)


if __name__ == "__main__":
    typer.run(main)
