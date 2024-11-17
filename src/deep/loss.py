import numpy as np


class MSE:
    @staticmethod
    def loss_function(predictions: np.array, labels: np.array) -> float:
        diff = predictions - labels
        return 0.5 * sum(diff * diff)[0]

    @staticmethod
    def loss_derivative(predictions: np.array, labels: np.array) -> np.array:
        return predictions - labels
