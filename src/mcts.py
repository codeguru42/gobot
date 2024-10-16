import random
from typing import Self

from go.goboard import GameState, Move
from go.gotypes import Player


class MCTSNode:
    def __init__(self, game_state: GameState, parent: Self = None, move: Move = None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {Player.BLACK: 0, Player.WHITE: 0}
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = list(game_state.legal_moves())

    def add_random_child(self) -> Self:
        index = random.randint(0, len(self.children) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner: Player):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self) -> bool:
        return len(self.unvisited_moves) > 0

    def is_terminal(self) -> bool:
        return self.game_state.is_over()

    def winning_frac(self, player: Player) -> float:
        return self.win_counts[player] / self.num_rollouts
