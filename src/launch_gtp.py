import sys

import typer


def main() -> None:
    while True:
        line = sys.stdin.readline()
        print(line)


if __name__ == "__main__":
    typer.run(main)
