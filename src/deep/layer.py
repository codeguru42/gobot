from typing import Self, Optional

from deep.sigmoid import sigmoid, sigmoid_prime


class Layer:
    def __init__(self):
        self.params = []
        self.previous: Optional[Layer] = None
        self.next: Optional[Layer] = None
        self.input_data = None
        self.output_data = None
        self.input_delta = None
        self.output_delta = None

    def connect(self, layer: Self):
        self.previous = layer
        layer.next = self

    def forward(self):
        raise NotImplementedError

    def get_foward_input(self):
        if self.previous is None:
            return self.input_data
        else:
            return self.previous.output_data

    def backward(self):
        raise NotImplementedError

    def get_backward_input(self):
        if self.next is None:
            return self.input_delta
        else:
            return self.next.output_delta

    def clear_deltas(self):
        pass

    def update_params(self, learning_rate):
        pass

    def describe(self):
        raise NotImplementedError


class ActivationLayer(Layer):
    def __init__(self, input_dim: int):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = input_dim

    def forward(self):
        data = self.get_foward_input()
        self.output_data = sigmoid(data)

    def backward(self):
        delta = self.get_backward_input()
        data = self.get_foward_input()
        self.output_delta = delta * sigmoid_prime(data)

    def describe(self):
        print(f"|-- {self.__class__.__name__}")
        print(f"  |-- dimensions: ({self.input_dim},{self.output_dim})")
