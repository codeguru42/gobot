import json
import multiprocessing
import tarfile
from pathlib import Path
from typing import Iterable, IO

import numpy as np
import typer

from encoders.base import get_encoder_by_name
from go.goboard import GameState
from metadata import GameMetadata
from replay import visit_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens
from utils.json_encoders import CustomJSONEncoder


def extract_files(file: Path) -> Iterable[IO[bytes]]:
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
    tarfile_path: Path,
    contents: Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]],
    output_directory: Path,
):
    typer.echo(f"Saving encodings for {tarfile_path}")
    npz_path = output_directory / f"{tarfile_path.stem}.npz"
    data, games = process_all_encodings(npz_path, contents)
    output_directory.mkdir(parents=True, exist_ok=True)
    np.savez(npz_path, **data)
    metadata_path = output_directory / tarfile_path.stem
    with open(metadata_path.with_suffix(".json"), "w") as metadata_file:
        json.dump(games, metadata_file, cls=CustomJSONEncoder, indent=2)


def process_all_encodings(
    npz_path: Path,
    contents: Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]],
) -> tuple[dict[Path, np.ndarray], list[GameMetadata]]:
    data = {}
    games = []
    for file_name, encs in contents:
        try:
            subdata, move_count = process_encodings(file_name, encs)
            data.update(subdata)
            games.append(
                GameMetadata(
                    npz_name=npz_path.name,
                    features_array=f"features/{file_name}",
                    labels_array=f"labels/{file_name}",
                    move_count=move_count,
                )
            )
        except Exception as e:
            typer.echo(f"ERROR: Skipping {file_name}")
            typer.echo(e)
    return data, games


def process_encodings(
    sgf_path: str,
    encodings,
) -> tuple[dict[str, np.ndarray], int]:
    features, labels = zip(*encodings)
    feature_path = f"features/{sgf_path}"
    label_path = f"labels/{sgf_path}"
    data = {
        str(feature_path): np.array(features),
        str(label_path): np.array(labels),
    }
    return data, len(features)


def save_all_encodings(args: tuple[Path, Path]):
    tarfile_path, encodings_directory = args
    extracted_files = extract_files(tarfile_path)
    encodings = encode_all_files(extracted_files)
    save_encodings(tarfile_path, encodings, encodings_directory)


def main(base_directory: Path):
    data_directory = base_directory / "data"
    encodings_directory = base_directory / "encodings"
    with multiprocessing.Pool() as pool:
        pool.map(
            save_all_encodings,
            [
                (tarfile_path, encodings_directory)
                for tarfile_path in data_directory.glob("*.tar.gz")
            ],
        )


if __name__ == "__main__":
    typer.run(main)
