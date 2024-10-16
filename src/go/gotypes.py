from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Self


class Player(Enum):
    BLACK = 1
    WHITE = 2

    @property
    def other(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def neighbors(self) -> Iterable[Self]:
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
