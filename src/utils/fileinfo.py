from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileInfo:
    tarfile: Path
    filename: str
