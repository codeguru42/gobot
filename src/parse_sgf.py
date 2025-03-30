import typer
from pathlib import Path
from typing import Optional

from sgf.parser import Collection, GameTree, Node, Property, Sequence, UnexpectedTokenException, parse_sgf
from sgf.tokenizer import tokens

app = typer.Typer(
    name="parse-sgf",
    help="Parse and visualize SGF (Smart Game Format) files",
    add_completion=False,
)


def visualize_node(node: Node, indent: str = "") -> None:
    """Visualize a single node in the SGF tree."""
    print(f"{indent}Node:")
    print(f"{indent}  Properties:")
    visualize_properties(node.properties, indent + "    ")


def visualize_properties(properties: list[Property], indent: str = "") -> None:
    """Visualize a list of properties."""
    for prop in properties:
        print(f"{indent}- Ident: {prop.ident.token}")
        print(f"{indent}  Values: {[v.token for v in prop.values]}")


def visualize_sequence(sequence: Sequence, indent: str = "") -> None:
    """Visualize a sequence of nodes in the SGF tree."""
    print(f"{indent}Sequence:")
    for node in sequence.nodes:
        visualize_node(node, indent + "  ")


def visualize_game_tree(tree: GameTree, indent: str = "") -> None:
    """Visualize a game tree in the SGF tree."""
    print(f"{indent}GameTree:")
    print(f"{indent}  Mainline:")
    visualize_sequence(tree.mainline, indent + "    ")

    if tree.variations:
        print(f"{indent}  Variations:")
        for i, variation in enumerate(tree.variations, 1):
            print(f"{indent}    Variation {i}:")
            visualize_game_tree(variation, indent + "      ")


def visualize_collection(collection: Collection) -> None:
    """Visualize the entire SGF collection."""
    print("SGF Collection:")
    for i, game in enumerate(collection.games, 1):
        print(f"\nGame {i}:")
        visualize_game_tree(game, "  ")


def parse_and_visualize_sgf(filename: Path) -> None:
    """Parse and visualize an SGF file."""
    try:
        with open(filename, "r") as f:
            content = f.read()

        # Tokenize and parse the SGF content
        token_stream = tokens(content)
        collection = parse_sgf(token_stream)

        # Visualize the parsed structure
        visualize_collection(collection)

    except FileNotFoundError:
        typer.echo(f"Error: File '{filename}' not found", err=True)
        raise typer.Exit(1)
    except UnexpectedTokenException as e:
        typer.echo(f"Error parsing SGF file: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def main(
    filename: Path = typer.Argument(
        help="Path to the SGF file to parse",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
) -> None:
    """
    Parse and visualize the structure of an SGF file.
    """
    parse_and_visualize_sgf(filename)


if __name__ == "__main__":
    app()
