from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class GameMetadata:
    npz_path: Path
    features_array: str
    labels_array: str
    move_count: int


def decode_metadata(data):
    match data:
        case {
            "npz_path": npz,
            "features_array": features,
            "labels_array": labels,
            "move_count": move_count,
        }:
            return GameMetadata(
                npz_path=Path(npz),
                features_array=features,
                labels_array=labels,
                move_count=move_count,
            )
        case _:
            raise ValueError(f"Unknown metadata format: {data}")


def total_move_count(metadata: Iterable[GameMetadata]) -> int:
    return sum(item.move_count for item in metadata)


def total_steps(metadata: Iterable[GameMetadata], batch_size: int) -> int:
    return sum(item.move_count // batch_size for item in metadata)