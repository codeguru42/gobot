from typing import Self, Optional


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
