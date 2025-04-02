import tarfile
from pathlib import Path
from typing import Iterable

import typer

from parse_sgf import visualize_collection
from sgf.parser import parse_sgf, Collection
from sgf.tokenizer import tokens


def extract_files(input_directory: Path) -> Iterable[BufferedReader]:
    for file in input_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def parse_files(input_directory: Path) -> Iterable[Collection]:
    for f in extract_files(input_directory):
        content = f.read().decode("utf-8")
        yield parse_sgf(tokens(content))


def main(input_directory: Path, output_directory: Path):
    for collection in parse_files(input_directory):
        visualize_collection(collection)

if __name__ == "__main__":
    typer.run(main)
