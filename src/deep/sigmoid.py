import numpy as np


def sigmoid_double(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid(z: np.array) -> np.array:
    return np.vectorize(sigmoid_double)(z)


def predict(x: np.array, W: np.array, b: np.array) -> np.array:
    return sigmoid_double(np.dot(x, W) + b)


def sigmoid_prime_double(x: float) -> float:
    return sigmoid_double(x) * (1 - sigmoid_double(x))


def sigmoid_prime(z: np.array) -> np.array:
    return np.vectorize(sigmoid_prime_double)(z)
