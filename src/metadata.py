from dataclasses import dataclass
from pathlib import Path


@dataclass
class GameMetadata:
    tarfile: Path
    sgf_file: Path
    move_count: int


def decode_metadata(data):
    match data:
        case {"tarfile": tarfile, "sgf_file": sgf_file, "move_count": move_count}:
            return GameMetadata(
                tarfile=Path(tarfile), sgf_file=Path(sgf_file), move_count=move_count
            )
        case _:
            raise ValueError(f"Unknown metadata format: {data}")
