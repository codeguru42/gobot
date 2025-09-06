import numpy as np

from encoders.base import Encoder
from go.goboard import GameState
from go.gotypes import Point


class OnePlaneEncoder(Encoder):
    def __init__(self, board_size: tuple[int, int]):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):
        return "oneplane"

    def encode(self, game_state: GameState) -> np.ndarray:
        board_matrix = np.zeros(self.shape(), dtype=np.uint8)
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix

    def encode_point(self, point: Point) -> np.ndarray:
        index = self.board_width * (point.row - 1) + (point.col - 1)
        move_one_hot = np.zeros(self.num_points(), dtype=np.uint8)
        move_one_hot[index] = 1
        return move_one_hot

    def decode_point_index(self, index: int) -> Point:
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self) -> int:
        return self.board_width * self.board_height

    def shape(self) -> tuple[int, int, int]:
        return self.num_planes, self.board_width, self.board_height


def create(board_size: int | tuple[int, int]) -> OnePlaneEncoder:
    return OnePlaneEncoder(board_size)
