import itertools
import json
import random
from pathlib import Path
from typing import Iterable, Sequence, Annotated

import keras
import numpy as np
import typer
from keras.api.callbacks import BackupAndRestore

from metadata import decode_metadata, GameMetadata, total_move_count
from models import get_small_model
from utils.json_encoders import CustomJSONEncoder


def sample_data[T](
    data: Sequence[T], k: int, sample_file: Path
) -> tuple[list[T], list[T]]:
    if sample_file.exists():
        with sample_file.open("r") as f:
            testing = json.load(f, object_hook=decode_metadata)
    else:
        testing = random.sample(data, k)
        with sample_file.open("w") as f:
            json.dump(testing, f, cls=CustomJSONEncoder, indent=2)
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
    for feature, label in data:
        while feature.shape[0] > batch_size:
            yield feature[:batch_size], label[:batch_size]
            feature = feature[batch_size:]
            label = label[batch_size:]


def load_encodings(
    metadata: Iterable[GameMetadata],
) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    while True:
        for item in metadata:
            npz = np.load(item.npz_path)
            yield npz.get(item.features_array), npz.get(item.labels_array)


def train(
    model: keras.models.Model,
    training_data: Iterable[tuple[np.ndarray, np.ndarray]],
    validation_data: Iterable[tuple[np.ndarray, np.ndarray]],
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


def evaluate(
    model: keras.Model,
    testing_data: Iterable[tuple[np.ndarray, np.ndarray]],
    batch_size: int,
):
    typer.echo("Evaluating model")
    testing_batches = batches(testing_data, batch_size)
    score = model.evaluate(testing_batches, verbose=0)
    typer.echo(f"\nTest loss: {score[0]}")
    typer.echo(f"Test accuracy: {score[1]}")


def load_metadata(encodings_directory):
    for file_path in encodings_directory.glob("*.json"):
        with file_path.open("r") as file:
            yield from json.load(file, object_hook=decode_metadata)


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
        metadata,
        test_size,
        test_sample_file,
    )
    validation_sample_file = base_directory / "validation.json"
    training_files, validation_files = sample_data(
        list(training_files), test_size, validation_sample_file
    )
    typer.echo(
        f"\nTraining {len(training_files)} games with {total_move_count(training_files)} moves"
    )
    typer.echo(
        f"Testing {len(testing_files)} games with {total_move_count(testing_files)} moves"
    )
    typer.echo(
        f"Validation {len(validation_files)} games with {total_move_count(validation_files)} moves"
    )
    input_shape = (1, 19, 19)
    training_data = load_encodings(training_files)
    validation_data = load_encodings(validation_files)
    testing_data = load_encodings(testing_files)
    model = get_small_model(input_shape)
    model = train(model, training_data, validation_data, batch_size, model_directory)
    evaluate(model, testing_data, batch_size)
    model_directory.mkdir(parents=True, exist_ok=True)
    model_file = model_directory / "final.keras"
    model.save(model_file)


if __name__ == "__main__":
    typer.run(main)
