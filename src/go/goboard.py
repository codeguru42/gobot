import copy
from dataclasses import dataclass
from typing import Self, Iterable, Optional, Tuple, Union, Generator

from go import zobrist
from go.gotypes import Point, Player
from scoring import compute_game_result


@dataclass
class Move:
    point: Point = None
    is_pass: bool = False
    is_resign: bool = False

    @property
    def is_play(self):
        return self.point is not None

    @classmethod
    def play(cls, point) -> Self:
        return cls(point=point, is_pass=False, is_resign=False)

    @classmethod
    def pass_turn(cls) -> Self:
        return cls(is_pass=True)

    @classmethod
    def resign(cls) -> Self:
        return cls(is_resign=True)


@dataclass
class GoString:
    color: Player
    stones: frozenset[Point]
    liberties: frozenset[Point]

    def __init__(
        self, color: Player, stones: Iterable[Point], liberties: Iterable[Point]
    ):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point: Point) -> Self:
        new_liberties = self.liberties - {point}
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point: Point) -> Self:
        new_liberties = self.liberties | {point}
        return GoString(self.color, self.stones, new_liberties)

    def merge_with(self, go_string: Self) -> Self:
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones,
        )

    @property
    def num_liberties(self) -> int:
        return len(self.liberties)

    def __eq__(self, other):
        return (
            isinstance(other, GoString)
            and self.color == other.color
            and self.stones == other.stones
            and self.liberties == other.liberties
        )


class Board:
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid: dict[Point, Optional[GoString]] = {}
        self._hash = zobrist.EMPTY_BOARD

    def __eq__(self, __value):
        return isinstance(__value, Board) and self._hash == __value._hash

    def is_on_grid(self, point: Point) -> bool:
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point: Point) -> Optional[Player]:
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point) -> Optional[GoString]:
        return self._grid.get(point)

    def place_stone(self, player: Player, point: Point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merge_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        self._hash ^= zobrist.HASH_CODE[point, player]

        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(replacement)
            else:
                self._remove_string(other_color_string)

    def _remove_string(self, string: GoString):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid[point] = None
            self._hash ^= zobrist.HASH_CODE[point, string.color]

    def _replace_string(self, new_string):
        for point in new_string.stones:
            self._grid[point] = new_string

    def zobrist_hash(self):
        return self._hash


class GameState:
    def __init__(
        self,
        board: Board,
        next_player: Player,
        previous: Optional[Self] = None,
        move: Optional[Move] = None,
    ):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states
                | {(previous.next_player, previous.board.zobrist_hash())}
            )
        self.last_move = move

    def apply_move(self, move: Move) -> Self:
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size: Union[Tuple[int, int], int]) -> Self:
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return cls(board, Player.BLACK)

    def is_over(self) -> bool:
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(self, player: Player, move: Move) -> bool:
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    def does_move_violate_ko(self, player: Player, move: Move) -> bool:
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move: Move) -> bool:
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
            self.board.get(move.point) is None
            and not self.is_move_self_capture(self.next_player, move)
            and not self.does_move_violate_ko(self.next_player, move)
        )

    def legal_moves(self) -> Generator[Move, None, None]:
        for r in range(1, self.board.num_rows + 1):
            for c in range(1, self.board.num_cols + 1):
                m = Move.play(Point(r, c))
                if self.is_valid_move(m):
                    yield m
        yield Move.pass_turn()
        yield Move.resign()

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player

        game_result = compute_game_result(self)
        return game_result.winner
