from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GameMetadata:
    npz_path: Path
    features_array: str
    labels_array: str
    move_count: int


def decode_metadata(data):
    match data:
        case {"npz_path": npz, "features_array": features, "labels_array": labels, "move_count": move_count}:
            return GameMetadata(
                npz_path=Path(npz),
                features_array=features,
                labels_array=labels,
                move_count=move_count,
            )
        case _:
            raise ValueError(f"Unknown metadata format: {data}")
