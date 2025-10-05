import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from utils.json_encoders import CustomJSONEncoder


@dataclass(frozen=True)
class GameMetadata:
    npz_name: str
    features_array: str
    labels_array: str
    move_count: int


def decode_metadata(data):
    match data:
        case {
            "npz_name": npz,
            "features_array": features,
            "labels_array": labels,
            "move_count": move_count,
        }:
            return GameMetadata(
                npz_name=npz,
                features_array=features,
                labels_array=labels,
                move_count=move_count,
            )
        case _:
            raise ValueError(f"Unknown metadata format: {data}")


def read_metadata(metadata_path: Path) -> list[GameMetadata]:
    try:
        with metadata_path.open("r") as f:
            return json.load(f, object_hook=decode_metadata)
    except ValueError as e:
        raise ValueError(f"ERROR: Unable to decode {metadata_path}", e)


def save_metadata(metadata: Iterable[GameMetadata], metadata_path: Path) -> None:
    with metadata_path.open("w") as f:
        json.dump(list(metadata), f, cls=CustomJSONEncoder, indent=2)


def load_metadata(encodings_directory):
    for file_path in encodings_directory.glob("*.json"):
        yield from read_metadata(file_path)


def total_move_count(metadata: Iterable[GameMetadata]) -> int:
    return sum(item.move_count for item in metadata)


def total_steps(metadata: Iterable[GameMetadata], batch_size: int) -> int:
    return sum(item.move_count // batch_size for item in metadata)
