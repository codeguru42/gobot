from dataclasses import dataclass


@dataclass
class GameMetadata:
    name: str
    move_count: int


@dataclass
class TarfileMetadata:
    path: str
    game_count: int
    games: list[GameMetadata]

    @property
    def move_count(self):
        return sum(game.move_count for game in self.games)


def decode_metadata(data):
    match data:
        case {"path": path, "game_count": game_count, "games": games}:
            return TarfileMetadata(
                path=path,
                game_count=game_count,
                games=games,
            )
        case {"name": name, "move_count": move_count}:
            return GameMetadata(name=name, move_count=move_count)
        case _:
            raise ValueError(f"Unknown metadata format: {data}")
