from typing import Self, Iterable

from gobot.gotypes import Point


class Move:
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return cls(point=point, is_pass=False, is_resign=False)

    @classmethod
    def pass_turn(cls):
        return cls(is_pass=True)

    @classmethod
    def resign(cls):
        return cls(is_resign=True)


class GoString:
    def __init__(self, color, stones: Iterable[Point], liberties: Iterable[Point]):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point: Point):
        self.liberties.remove(point)

    def add_liberty(self, point: Point):
        self.liberties.add(point)

    def merge_with(self, go_string: Self):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (go_string.liberties | go_string.liberties) - combined_stones,
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return (
            isinstance(other, GoString)
            and self.color == other.color
            and self.stones == other.stones
            and self.liberties == other.liberties
        )
