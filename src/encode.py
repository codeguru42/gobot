import itertools
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
        typer.echo(f"Extracting {file.name}")
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def parse_file(sgf_file: Optional[IO[bytes]]) -> Collection:
    typer.echo("****")
    typer.echo(f"Parsing {sgf_file.name}")
    content = sgf_file.read().decode("utf-8")
    return parse_sgf(tokens(content))


def replay_game(
    collection: Collection,
) -> Iterable[Iterable[GameState]]:
    return visit_collection(collection)


def encode_game(games) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    for game in games:
        for game_state in game:
            encoder = get_encoder_by_name(
                "oneplane", (game_state.board.num_cols, game_state.board.num_rows)
            )
            if game_state.last_move is not None and game_state.last_move.is_play:
                yield (
                    encoder.encode(game_state),
                    encoder.encode_point(game_state.last_move.point),
                )


def encode_all(
    sgf_files: Iterable[Optional[IO[bytes]]],
) -> Iterable[tuple[str, Iterable[tuple[np.ndarray, np.ndarray]]]]:
    for file in sgf_files:
        collection = parse_file(file)
        game_states = replay_game(collection)
        yield file.name, encode_game(game_states)


def save_encodings(
    encodings: Iterable[tuple[str, Iterable[tuple[np.ndarray, np.ndarray]]]],
    output_directory: Path,
) -> None:
    feature_base = output_directory / "features"
    label_base = output_directory / "labels"
    for file_name, encs in encodings:
        try:
            typer.echo(f"Saving {file_name}")
            features, labels = zip(*encs)
            sgf_path = Path(file_name)
            feature_path = feature_base / sgf_path.parent
            feature_path.mkdir(parents=True, exist_ok=True)
            label_path = label_base / sgf_path.parent
            label_path.mkdir(parents=True, exist_ok=True)
            np.save(feature_path / sgf_path.stem, np.concatenate(features))
            np.save(label_path / sgf_path.stem, np.concatenate(labels))
        except Exception as e:
            typer.echo("ERROR: Skipping.")
            typer.echo(e)


def main(input_directory: Path, output_directory: Path):
    typer.echo(f"Extracting files from {input_directory}")
    sgf_files = extract_files(input_directory)
    typer.echo("Encoding games...")
    encodings = encode_all(sgf_files)
    typer.echo("Saving encodings...")
    save_encodings(encodings, output_directory)


if __name__ == "__main__":
    typer.run(main)
