import sys

import typer


def interpret_command(line):
    match line.strip().split():
        case ["quit"]:
            sys.exit(0)
        case _:
            typer.echo("Unknown command")
