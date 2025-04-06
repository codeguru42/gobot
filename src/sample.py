import random
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass
class FileInfo:
    tarfile: str
    filename: str


def sample[T](data: Sequence[T], k: int) -> tuple[Iterable[T], Iterable[T]]:
    training = random.sample(data, k)
    testing = list(set(data) - set(training))
    return training, testing


def get_sgf_list(data_directory: Path) -> Iterable[FileInfo]: 
    for file in data_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield FileInfo(file.name, member.name)
