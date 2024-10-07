from black.cache import dataclass

from gobot.gotypes import Player, Point


@dataclass
class GameResult:
    black: float
    white: float
    komi: float

    @property
    def winner(self):
        if self.black > self.white + self.komi:
            return Player.BLACK
        return Player.WHITE

    @property
    def winning_margin(self):
        return abs(self.black - (self.white + self.komi))

    def __str__(self):
        w = self.white - self.komi
        if self.black > w:
            return f"B+{self.black-w:.1f}"
        return f"W+{w-self.black:.1f}"


class Territory:
    def __init__(self, territory_map: dict[Point, str]):
        self.black_territory = 0
        self.white_territory = 0
        self.black_stones = 0
        self.white_stones = 0
        self.dame = 0
        self.dame_points = []
        for point, status in territory_map.items():
            match status:
                case Player.BLACK:
                    self.black_stones += 1
                case Player.WHITE:
                    self.white_stones += 1
                case "territory_b":
                    self.black_territory += 1
                case "territory_w":
                    self.white_territory += 1
                case "dame":
                    self.dame += 1
                    self.dame_points.append(point)


def _collect_region(
    start_pos: Point, board: "Board", visited: dict[Point, bool] = None
) -> tuple[list, set]:
    if visited is None:
        visited = {}
    if start_pos in visited:
        return [], set()
    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    here = board.get(start_pos)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta_r, delta_c in deltas:
        next_p = Point(start_pos.row + delta_r, start_pos.col + delta_c)
        if not board.is_on_grid(next_p):
            continue
        neighbor = board.get(next_p)
        if neighbor == here:
            points, borders = _collect_region(next_p, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


def evaluate_territory(board: "Board") -> Territory:
    status = {}
    for r in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            p = Point(row=r, col=c)
            if p in status:
                continue
            stone = board.get(p)
            if stone is not None:
                status[p] = stone
            else:
                group, neighbors = _collect_region(p, board)
                if len(neighbors) == 1:
                    neighbor_stone = neighbors.pop(0)
                    stone_str = "b" if neighbor_stone == Player.BLACK else "w"
                    fill_with = f"territory_{stone_str}"
                else:
                    fill_with = "dame"
                for pos in group:
                    status[pos] = fill_with
    return Territory(status)


def compute_game_result(game_state: "GameState") -> GameResult:
    territory = evaluate_territory(game_state.board)
    return GameResult(
        black=territory.black_territory + territory.black_stones,
        white=territory.white_territory + territory.white_stones,
        komi=7.5,
    )
