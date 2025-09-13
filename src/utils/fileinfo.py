from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileInfo:
    tarfile: Path
    filename: str


def decode_file_info(data):
    return FileInfo(tarfile=data['tarfile'], filename=data['filename'])
