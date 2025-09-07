import tarfile
from pathlib import Path
from typing import Iterable, IO

import numpy as np
import typer

from encoders.base import get_encoder_by_name
from go.goboard import GameState
from replay import visit_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens


def extract_files(input_directory: Path) -> Iterable[IO[bytes]]:
    for file in input_directory.glob("*.tar.gz"):
        typer.echo(f"Extracting {file.name}")
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def parse_file(sgf_file: IO[bytes]) -> Collection:
    content = sgf_file.read().decode("utf-8")
    return parse_sgf(tokens(content))


def replay_game(
    collection: Collection,
) -> Iterable[Iterable[GameState]]:
    return visit_collection(collection)


def encode_games(
    games: Iterable[Iterable[GameState]],
) -> Iterable[tuple[np.ndarray, np.ndarray]]:
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


def encode_file(
    sgf_file: IO[bytes],
) -> list[tuple[np.ndarray, np.ndarray]]:
    collection = parse_file(sgf_file)
    game_states = replay_game(collection)
    return list(encode_games(game_states))


def encode_all_files(
    sgf_files: Iterable[IO[bytes]],
) -> Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]]:
    for file in sgf_files:
        yield file.name, encode_file(file)


def save_encodings(
    encodings: Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]],
    output_directory: Path,
) -> None:
    data = {}
    for file_name, encs in encodings:
        try:
            typer.echo(f"Saving {file_name}")
            features, labels = zip(*encs)
            sgf_path = Path(file_name)
            feature_path = sgf_path.parent / f'features_{sgf_path.stem}'
            data[str(feature_path)] = features
            label_path = sgf_path.parent / f'labels_{sgf_path.stem}'
            data[str(label_path)] = labels
        except Exception as e:
            typer.echo("ERROR: Skipping.")
            typer.echo(e)
    output_directory.mkdir(parents=True, exist_ok=True)
    np.savez(output_directory / "encodings.npz", **data)


def main(input_directory: Path):
    output_directory = input_directory / "encodings"
    typer.echo(f"Extracting files from {input_directory}")
    sgf_files = extract_files(input_directory)
    typer.echo("Encoding games...")
    encodings = encode_all_files(sgf_files)
    typer.echo("Saving encodings...")
    save_encodings(encodings, output_directory)


if __name__ == "__main__":
    typer.run(main)
