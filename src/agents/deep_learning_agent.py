import numpy as np

from agents.base import Agent
from agents.helpers import is_point_an_eye
from go.goboard import GameState, Move


class DeepLearningAgent(Agent):
    def __init__(self, model, encoder):
        super().__init__()
        self.model = model
        self.encoder = encoder

    def predict(self, game_state):
        encoded_state = self.encoder.encode(game_state)
        tensor = np.array([encoded_state])
        return self.model.predict(tensor)

    def select_move(self, game_state: GameState):
        move_count = self.encoder.board_width * self.encoder.board_height
        raw_probs = self.model.predict(game_state)
        eps = 1e-6
        clipped_probs = np.clip(raw_probs**3, eps, 1 - eps)
        probs = clipped_probs / np.sum(clipped_probs)
        candidates = np.arange(move_count)
        ranked_moves = np.random.choice(
            candidates, size=move_count, replace=False, p=probs
        )
        for i in ranked_moves:
            point = self.encoder.decode_point_index(i)
            move = Move.play(point)
            if game_state.is_valid_move(move) and not is_point_an_eye(
                game_state.board,
                point,
                game_state.next_player,
            ):
                return move
        return Move.pass_turn()
