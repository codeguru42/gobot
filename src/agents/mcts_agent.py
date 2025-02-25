import math

from agents.base import Agent
from agents.naive import RandomBot
from go.goboard import GameState, Move
from go.gotypes import Player
from mcts import MCTSNode


def uct_score(
    parent_rollouts: float, child_rollouts: float, win_pct: float, temperature: float
) -> float:
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


class MCTSAgent(Agent):
    def __init__(
        self,
        num_rounds: int,
        temperature: float,
    ):
        super().__init__()
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state: GameState) -> Move:
        root = MCTSNode(game_state)
        self.perform_rollouts(root)
        return self.get_best_move(game_state.next_player, root)

    def perform_rollouts(self, root):
        for i in range(self.num_rounds):
            node = root
            while not node.can_add_child() and not node.is_terminal():
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

    def get_best_move(self, player, root):
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node: MCTSNode) -> MCTSNode:
        total_rollouts = sum(child.num_rollouts for child in node.children)
        best_score = -1.0
        best_child = None
        for child in node.children:
            score = uct_score(
                total_rollouts,
                child.num_rollouts,
                child.winning_frac(node.game_state.next_player),
                self.temperature,
            )
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_game(game_state: GameState) -> Player:
        bots = {
            Player.BLACK: RandomBot(
                game_state.board.num_rows, game_state.board.num_cols
            ),
            Player.WHITE: RandomBot(
                game_state.board.num_rows, game_state.board.num_cols
            ),
        }
        while not game_state.is_over():
            bot_move = bots[game_state.next_player].select_move(game_state)
            game_state = game_state.apply_move(bot_move)
        return game_state.winner()
