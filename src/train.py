import random
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import typer

from encode import encode_file


@dataclass(frozen=True)
class FileInfo:
    tarfile: str
    filename: str


def sample[T](data: Sequence[T], k: int) -> tuple[list[T], list[T]]:
    testing = random.sample(data, k)
    training = list(set(data) - set(testing))
    return training, testing


def get_sgf_files(data_directory: Path) -> Iterable[FileInfo]:
    for file in data_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield FileInfo(file.name, member.name)


def encode_from_file_info(
    files: Iterable[FileInfo],
) -> Iterable[Iterable[tuple[np.ndarray, np.ndarray]]]:
    for file_info in files:
        with tarfile.open(file_info.tarfile) as tar:
            sgf_file = tar.extractfile(file_info.filename)
            if sgf_file is None:
                continue
            yield encode_file(sgf_file)


def main(input_directory: Path):
    files = get_sgf_files(input_directory)
    training, testing = sample(list(files), 100)
    typer.echo(f"Training {len(training)} samples")
    typer.echo(f"Testing {len(testing)} samples")


if __name__ == "__main__":
    typer.run(main)
