import itertools
import json
import random
from pathlib import Path
from typing import Iterable, Sequence, Annotated

import keras
import numpy as np
import typer
from keras.api.callbacks import BackupAndRestore

from metadata import decode_metadata
from models import get_large_model
from utils.fileinfo import FileInfo, decode_file_info
from utils.json_encoders import CustomJSONEncoder


def sample_data[T](
    data: Sequence[T], k: int, sample_file: Path
) -> tuple[list[T], list[T]]:
    if sample_file.exists():
        with sample_file.open("r") as f:
            testing = json.load(f, object_hook=decode_file_info)
    else:
        testing = random.sample(data, k)
        with sample_file.open("w") as f:
            json.dump(testing, f, cls=CustomJSONEncoder)
    training = list(set(data) - set(testing))
    return training, testing


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    """Collect data into non-overlapping fixed-length chunks or blocks."""
    # grouper('ABCDEFG', 3, fillvalue='x') → ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') → ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
    iterators = [iter(iterable)] * n
    match incomplete:
        case "fill":
            return itertools.zip_longest(*iterators, fillvalue=fillvalue)
        case "strict":
            return zip(*iterators, strict=True)
        case "ignore":
            return zip(*iterators)
        case _:
            raise ValueError("Expected fill, strict, or ignore")


def batches(data, batch_size):
    for batch in grouper(data, batch_size, incomplete="ignore"):
        features = []
        labels = []
        for feature, label in batch:
            features.append(feature)
            labels.append(label)
        yield np.array(features), np.array(labels)


def train(
    model: keras.models.Model,
    training_data: Iterable[np.ndarray],
    validation_data: Iterable[np.ndarray],
    batch_size: int,
    output_directory: Path,
) -> keras.Model:
    typer.echo("Training model")

    model.compile(
        loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"]
    )
    model.fit(
        batches(training_data, batch_size),
        validation_data=validation_data,
        epochs=15,
        verbose=2,
        callbacks=[BackupAndRestore(output_directory, delete_checkpoint=False)],
    )
    return model


def evaluate(model: keras.Model, testing_data: Iterable[np.ndarray], batch_size: int):
    typer.echo("Evaluating model")
    testing_batches = batches(testing_data, batch_size)
    score = model.evaluate(testing_batches, verbose=0)
    typer.echo(f"\nTest loss: {score[0]}")
    typer.echo(f"Test accuracy: {score[1]}")


def load_metadata(encodings_directory):
    for file_path in encodings_directory.glob("*.json"):
        yield json.load(file_path, object_hook=decode_metadata())


def main(
    base_directory: Path,
    test_size: Annotated[int, typer.Option("--test_size")] = 100,
    batch_size: Annotated[int, typer.Option("--batch_size")] = 64,
):
    encodings_directory = base_directory / "encodings"
    model_directory = base_directory / "model"
    metadata = list(load_metadata(encodings_directory))
    test_sample_file = base_directory / "test.json"
    training_files, testing_files = sample_data(
        list(files), test_size, test_sample_file
    )
    validation_sample_file = base_directory / "validation.json"
    training_files, validation_files = sample_data(
        list(training_files), test_size, validation_sample_file
    )
    typer.echo(f"\nTraining {len(training_files)} games")
    typer.echo(f"Testing {len(testing_files)} games")
    typer.echo(f"Validation {len(validation_files)} games")
    input_shape = (1, 19, 19)
    model = get_large_model(input_shape)
    model = train(model, training_files, validation_files, batch_size, model_directory)
    evaluate(model, testing_files, batch_size)
    model_directory.mkdir(parents=True, exist_ok=True)
    model_file = model_directory / "final.keras"
    model.save(model_file)


if __name__ == "__main__":
    typer.run(main)
