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
