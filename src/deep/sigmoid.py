import numpy as np


def sigmoid_double(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid(z: np.array) -> np.array:
    return np.vectorize(sigmoid_double)(z)


def predict(x: np.array, W: np.array, b: np.array) -> np.array:
    return sigmoid_double(np.dot(x, W) + b)
