import tarfile
from pathlib import Path

import typer


def extract_files(input_directory: Path):
    for file in input_directory.glob("*.tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    yield tar.extractfile(member)


def main(input_directory: Path, output_directory: Path):
    for f in extract_files(input_directory):
        print(f.read())


if __name__ == "__main__":
    typer.run(main)
