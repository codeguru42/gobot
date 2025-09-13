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
