import random
from typing import Iterable, MutableSequence


def sample[T](data: MutableSequence[T], k: int) -> tuple[Iterable[T], Iterable[T]]:
    training = random.sample(data, k)
    testing = list(set(data) - set(training))
    return training, testing
