import itertools
import json
import random
import tarfile
from pathlib import Path
from typing import Iterable, Sequence, Annotated

import keras
import numpy as np
import typer
from keras.api.callbacks import BackupAndRestore

from encode import encode_file
from models import get_large_model
from utils.fileinfo import FileInfo
from utils.json_decoders import decode_file_info
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
        with tarfile.open(file_info.tarfile) as tar:
            sgf_file = tar.extractfile(file_info.filename)
            if sgf_file is None:
                continue
            yield from encode_file(sgf_file)


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
    training_files: Iterable[FileInfo],
    validation_files: Iterable[FileInfo],
    batch_size: int,
    output_directory: Path,
) -> keras.Model:
    typer.echo("Training model")
    training_data = encode_from_file_info(training_files)
    validation_data = encode_from_file_info(validation_files)

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


def evaluate(model: keras.Model, testing_files: Iterable[FileInfo], batch_size: int):
    typer.echo("Evaluating model")
    testing_data = encode_from_file_info(testing_files)
    testing_batches = batches(testing_data, batch_size)
    score = model.evaluate(testing_batches, verbose=0)
    typer.echo(f"\nTest loss: {score[0]}")
    typer.echo(f"Test accuracy: {score[1]}")


def main(
    input_directory: Path,
    output_directory: Path,
    test_size: Annotated[int, typer.Option("--test_size")] = 100,
    batch_size: Annotated[int, typer.Option("--batch_size")] = 64,
):
    files = get_sgf_files(input_directory)
    test_sample_file = input_directory / "test.json"
    training, testing = sample_data(list(files), test_size, test_sample_file)
    validation_sample_file = input_directory / "test.json"
    training, validation = sample_data(
        list(training), test_size, validation_sample_file
    )
    typer.echo(f"\nTraining {len(training)} samples")
    typer.echo(f"Testing {len(testing)} samples")
    typer.echo(f"Validation {len(validation)} samples")
    input_shape = (1, 19, 19)
    model = get_large_model(input_shape)
    model = train(model, training, validation, batch_size, output_directory)
    evaluate(model, testing, batch_size)
    output_directory.parent.mkdir(parents=True, exist_ok=True)
    model_file = output_directory / "final.keras"
    model.save(model_file)


if __name__ == "__main__":
    typer.run(main)
