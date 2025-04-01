from pathlib import Path

import typer

def read_files(input_directory: Path):
    for file in input_directory.glob("*.tar.gz"):
        print(file.name)


def main(input_directory: Path, output_directory: Path):
    read_files(input_directory)


if __name__ == "__main__":
    typer.run(main)
