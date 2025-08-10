import sys

import typer

from gtp.commands import interpret_command


def main() -> None:
    while True:
        line = sys.stdin.readline()
        interpret_command(line)


if __name__ == "__main__":
    typer.run(main)
