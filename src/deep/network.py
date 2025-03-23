import random

import numpy as np

from deep.layer import Layer
from deep.loss import MSE


class SequentialNetwork:
    def __init__(self, loss=None):
        print("Initializing network...")
        self.layers: list[Layer] = []

        if loss is None:
            self.loss = MSE

    def add(self, layer):
        self.layers.append(layer)
        layer.describe()
        if len(self.layers) > 1:
            self.layers[-1].connect(self.layers[-2])

    def train(
        self,
        training_data,
        epochs: int,
        mini_batch_size: int,
        learning_rate: float,
        test_data=None,
    ):
        n = len(training_data)
        for epoch in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k : k + mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.train_batch(mini_batch, learning_rate)

            if test_data:
                n_test = len(test_data)
                print(f"Epoch {epoch}: {self.evaluate(test_data)} / {n_test}")
            else:
                print(f"Epoch {epoch} complete")

    def train_batch(self, mini_batch, learning_rate: float):
        self.forward_backward(mini_batch)
        self.update(mini_batch, learning_rate)

    def update(self, mini_batch, learning_rate):
        learning_rate = learning_rate / len(mini_batch)

        for layer in self.layers:
            layer.update_params(learning_rate)

        for layer in self.layers:
            layer.clear_deltas()

    def forward_backward(self, mini_batch):
        for x, y in mini_batch:
            self.layers[0].input_data = x
            for layer in self.layers:
                layer.forward()

            self.layers[-1].input_delta = self.loss.loss_derivative(
                self.layers[-1].output_data, y
            )
            for layer in reversed(self.layers):
                layer.backward()

    def single_forward(self, x: np.array) -> np.array:
        self.layers[0].input_data = x
        for layer in self.layers:
            layer.forward()
        return self.layers[-1].output_data

    def evaluate(self, test_data):
        test_results = [
            (np.argmax(self.single_forward(x)), np.argmax(y)) for x, y in test_data
        ]
        return sum(int(x == y) for x, y in test_results)
