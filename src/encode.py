import tarfile
from pathlib import Path
from typing import Iterable, IO, Optional

import numpy as np
import typer

from encoders.base import get_encoder_by_name
from go.goboard import GameState
from replay import visit_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens


def extract_files(input_directory: Path) -> Iterable[Optional[IO[bytes]]]:
    for file in input_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def parse_files(sgf_files: Iterable[Optional[IO[bytes]]]) -> Iterable[Collection]:
    for f in sgf_files:
        typer.echo(f"Parsing {f.name}")
        content = f.read().decode("utf-8")
        yield parse_sgf(tokens(content))


def replay_games(
    collections: Iterable[Collection],
) -> Iterable[Iterable[Iterable[GameState]]]:
    for collection in collections:
        yield visit_collection(collection)


def encode_game(games) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    for game in games:
        for game_state in game:
            encoder = get_encoder_by_name(
                "oneplane", (game_state.board.num_cols, game_state.board.num_rows)
            )
            if game_state.last_move is not None and game_state.last_move.is_play:
                typer.echo(f"Last move: {game_state.last_move}")
                yield (
                    encoder.encode(game_state),
                    encoder.encode_point(game_state.last_move.point),
                )


def encode_all(
    collections: Iterable[Collection],
) -> Iterable[Iterable[tuple[np.ndarray, np.ndarray]]]:
    for games in replay_games(collections):
        yield encode_game(games)


def main(input_directory: Path, output_directory: Path):
    sgf_files = extract_files(input_directory)
    collections = parse_files(sgf_files)
    for encs in encode_all(collections):
        for x, y in encs:
            print(x)
            print(y)


if __name__ == "__main__":
    typer.run(main)
