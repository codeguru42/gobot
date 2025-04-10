import random
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import keras
import numpy as np
import typer
from keras import Sequential

from encode import encode_file


@dataclass(frozen=True)
class FileInfo:
    tarfile: Path
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
                    yield FileInfo(file.absolute(), member.name)


def encode_from_file_info(
    files: Iterable[FileInfo],
) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    for file_info in files:
        typer.echo(f"Encoding {file_info}")
        with tarfile.open(file_info.tarfile) as tar:
            sgf_file = tar.extractfile(file_info.filename)
            if sgf_file is None:
                continue
            yield from encode_file(sgf_file)


def train(training_files: Iterable[FileInfo], testing_files: Iterable[FileInfo]):
    training_data = encode_from_file_info(training_files)
    testing_data = encode_from_file_info(testing_files)

    input_shape = (1, 19, 19)
    model = Sequential(
        [
            keras.layers.Input(input_shape),
            keras.layers.ZeroPadding2D(padding=3, data_format='channels_first'),
            keras.layers.Conv2D(48, (7, 7), data_format='channels_first'),
            keras.layers.Activation('relu'),

            keras.layers.ZeroPadding2D(padding=2, data_format='channels_first'),
            keras.layers.Conv2D(32, (5, 5), data_format='channels_first'),
            keras.layers.Activation('relu'),

            keras.layers.ZeroPadding2D(padding=2, data_format='channels_first'),
            keras.layers.Conv2D(32, (5, 5), data_format='channels_first'),
            keras.layers.Activation('relu'),

            keras.layers.ZeroPadding2D(padding=2, data_format='channels_first'),
            keras.layers.Conv2D(32, (5, 5), data_format='channels_first'),
            keras.layers.Activation('relu'),

            keras.layers.Flatten(),
            keras.layers.Dense(512),
            keras.layers.Activation('relu'),
        ]
    )

    model.compile()
    model.fit(
        training_data, batch_size=64, epochs=15, verbose=1, validation_data=testing_data
    )
    score = model.evaluate(testing_data, verbose=0)
    typer.echo(f"Test loss: {score[0]}")
    typer.echo(f"Test accuracy: {score[1]}")


def main(input_directory: Path):
    files = get_sgf_files(input_directory)
    training, testing = sample(list(files), 1)
    typer.echo(f"Training {len(training)} samples")
    typer.echo(f"Testing {len(testing)} samples")
    train(training, testing)


if __name__ == "__main__":
    typer.run(main)
