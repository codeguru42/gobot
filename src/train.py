import random
from pathlib import Path
from typing import Iterable, Sequence, Annotated

import keras
import numpy as np
import typer
from keras.api.callbacks import BackupAndRestore

from metadata import (
    GameMetadata,
    total_move_count,
    save_metadata,
    read_metadata,
    load_metadata,
)
from models import get_large_model


def sample_data[T](
    data: Sequence[T], k: int, sample_file: Path
) -> tuple[list[T], list[T]]:
    if sample_file.exists():
        testing = read_metadata(sample_file)
    else:
        testing = random.sample(data, k)
        save_metadata(testing, sample_file)
    training = list(set(data) - set(testing))
    return training, testing


def batches(data, batch_size):
    feature = np.empty((0, 1, 19, 19), dtype=np.int8)
    label = np.empty((0, 361), dtype=np.int8)
    for next_feature, next_label in data:
        feature = np.concatenate((feature, next_feature), axis=0)
        label = np.concatenate((label, next_label), axis=0)
        while feature.shape[0] >= batch_size:
            yield feature[:batch_size], label[:batch_size]
            feature = feature[batch_size:]
            label = label[batch_size:]


def load_encodings(
    metadata: Iterable[GameMetadata],
) -> Iterable[tuple[np.ndarray, np.ndarray]]:
    while True:
        for item in metadata:
            npz = np.load(item.npz_path)
            features = npz.get(item.features_array)
            labels = npz.get(item.labels_array)
            assert features.shape[0] == labels.shape[0] == item.move_count
            yield features, labels


def train(
    model: keras.models.Model,
    training_data: Iterable[tuple[np.ndarray, np.ndarray]],
    steps_count: int,
    validation_data: Iterable[tuple[np.ndarray, np.ndarray]],
    validation_steps: int,
    epochs: int,
    batch_size: int,
    output_directory: Path,
) -> keras.Model:
    typer.echo("Training model")

    model.compile(
        loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"]
    )
    model.fit(
        batches(training_data, batch_size),
        validation_data=batches(validation_data, batch_size),
        epochs=epochs,
        steps_per_epoch=steps_count,
        validation_steps=validation_steps,
        verbose=2,
        callbacks=[BackupAndRestore(output_directory, delete_checkpoint=False)],
    )
    return model


def evaluate(
    model: keras.Model,
    testing_data: Iterable[tuple[np.ndarray, np.ndarray]],
    steps_count: int,
    batch_size: int,
):
    typer.echo("Evaluating model")
    testing_batches = batches(testing_data, batch_size)
    score = model.evaluate(
        testing_batches,
        verbose=0,
        steps=steps_count,
    )
    typer.echo(f"\nTest loss: {score[0]}")
    typer.echo(f"Test accuracy: {score[1]}")


def main(
    base_directory: Path,
    epochs: Annotated[int, typer.Option("--epochs", "-e")] = 15,
    batch_size: Annotated[int, typer.Option("--batch_size", "-b")] = 64,
    test_proportion: Annotated[float, typer.Option("-t")] = 0.10,
    validation_proportion: Annotated[float, typer.Option("-v")] = 0.10,
):
    encodings_directory = base_directory / "encodings"
    model_directory = base_directory / "model"
    metadata = list(load_metadata(encodings_directory))
    test_count = int(test_proportion * len(metadata))
    test_sample_file = base_directory / "test.json"
    training_files, testing_files = sample_data(
        metadata,
        test_count,
        test_sample_file,
    )

    validation_sample_file = base_directory / "validation.json"
    validation_count = int(validation_proportion * len(metadata))
    training_files, validation_files = sample_data(
        training_files,
        validation_count,
        validation_sample_file,
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
    training_count = total_move_count(training_files)
    training_steps = training_count // batch_size
    validation_data = load_encodings(validation_files)
    validation_steps = total_move_count(validation_files) // batch_size
    testing_data = load_encodings(testing_files)
    testing_steps = total_move_count(testing_files) // batch_size
    model = get_large_model(input_shape)
    model = train(
        model,
        training_data,
        training_steps,
        validation_data,
        validation_steps,
        epochs,
        batch_size,
        model_directory,
    )
    evaluate(model, testing_data, testing_steps, batch_size)
    model_directory.mkdir(parents=True, exist_ok=True)
    model_file = model_directory / "final.keras"
    model.save(model_file)


if __name__ == "__main__":
    typer.run(main)
