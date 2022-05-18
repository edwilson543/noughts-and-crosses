import numpy as np

class NDimensionalNoughtsAndCrosses:
    """Base class to reflect the game play of a noughts and crosses game."""
    def __init__(self,
                 game_rows_m: int,
                 game_dimension_n: int,
                 winning_line_k: int):
        self.playing_grid = np.zeros(([game_rows_m] * game_dimension_n))
        self.winning_line_k = winning_line_k
