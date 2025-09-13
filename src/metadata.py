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
    return TarfileMetadata(
        path=data["path"],
        game_count=data["game_count"],
        games=list(
            decode_games(data["games"]),
        ),
    )


def decode_games(data):
    for game in data:
        yield GameMetadata(name=data["name"], move_count=game["move_count"])
