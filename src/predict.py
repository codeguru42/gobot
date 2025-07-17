from pathlib import Path

import numpy as np
import typer
from tensorflow.keras.models import load_model

from encoders.base import get_encoder_by_name
from go.goboard import GameState


def main(model_path: Path):
    model = load_model(model_path)
    game_state = GameState.new_game(19)
    encoder = get_encoder_by_name("oneplane", 19)
    encoded_game_state = encoder.encode(game_state)
    prediction = model(np.array((encoded_game_state,)))
    typer.echo(prediction)


if __name__ == "__main__":
    typer.run(main)
