import json
import tarfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, IO

import numpy as np
import typer

from encoders.base import get_encoder_by_name
from go.goboard import GameState
from replay import visit_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens


@dataclass
class GameMetadata:
    name: str
    move_count: int


@dataclass
class TarfileMetadata:
    path: str
    game_count: int
    games: list[GameMetadata]
    
    @property
    def move_count(self):
        return sum(game.move_count for game in self.games)


def extract_all_files(
    input_directory: Path,
) -> Iterable[tuple[Path, Iterable[IO[bytes]]]]:
    for file in input_directory.glob("*.tar.gz"):
        typer.echo(f"Extracting {file.name}")
        yield file, extract_files(file)


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


def encode_tar_files(
    extracted_files: Iterable[tuple[Path, Iterable[IO[bytes]]]],
) -> Iterable[tuple[Path, Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]]]]:
    for tar_file, sgf_files in extracted_files:
        yield tar_file, encode_all_files(sgf_files)


def save_all_encodings(
    encodings: Iterable[
        tuple[Path, Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]]]
    ],
    output_directory: Path,
) -> None:
    for tarfile_path, contents in encodings:
        save_encodings(tarfile_path, contents, output_directory)


def save_encodings(
    tarfile_path: Path,
    contents: Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]],
    output_directory: Path,
):
    typer.echo(f"Saving encodings for {tarfile_path}")
    data, games = process_all_encodings(contents)
    output_directory.mkdir(parents=True, exist_ok=True)
    npz_path = output_directory / tarfile_path.stem
    np.savez(npz_path, **data)
    metadata_path = output_directory / tarfile_path.stem
    metadata = TarfileMetadata(str(tarfile_path), len(games), games)
    with open(metadata_path.with_suffix(".json"), "w") as metadata_file:
        json.dump(asdict(metadata), metadata_file)


def process_all_encodings(
    contents: Iterable[tuple[str, list[tuple[np.ndarray, np.ndarray]]]],
) -> tuple[dict[Path, np.ndarray], list[GameMetadata]]:
    data = {}
    games = []
    for file_name, encs in contents:
        try:
            subdata, move_count = process_encodings(file_name, encs)
            data.update(subdata)
            games.append(GameMetadata(file_name, move_count))
        except Exception as e:
            typer.echo("ERROR: Skipping.")
            typer.echo(e)
            
    return data, games


def process_encodings(
    file_name: str,
    encodings,
) -> tuple[dict[str, np.ndarray], int]:
    features, labels = zip(*encodings)
    sgf_path = Path(file_name)
    feature_path = sgf_path.parent / f"features_{sgf_path.stem}"
    label_path = sgf_path.parent / f"labels_{sgf_path.stem}"
    data = {
        str(feature_path): np.concatenate(features),
        str(label_path): np.concatenate(labels),
    }
    return data, len(features)


def main(input_directory: Path):
    output_directory = input_directory / "encodings"
    typer.echo(f"Extracting files from {input_directory}")
    extracted_files = extract_all_files(input_directory)
    typer.echo("Encoding games...")
    encodings = encode_tar_files(extracted_files)
    typer.echo("Saving encodings...")
    save_all_encodings(encodings, output_directory)


if __name__ == "__main__":
    typer.run(main)
