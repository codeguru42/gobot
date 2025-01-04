from go.goboard import GameState
from go.gotypes import Point


class Encoder:
    def name(self):
        raise NotImplementedError()

    def encode(self, game_state: GameState):
        raise NotImplementedError()

    def encode_point(self, point: Point):
        raise NotImplementedError()

    def decode_point_index(self, index: int):
        raise NotImplementedError()

    def num_points(self):
        raise NotImplementedError()

    def shape(self):
        raise NotImplementedError()
