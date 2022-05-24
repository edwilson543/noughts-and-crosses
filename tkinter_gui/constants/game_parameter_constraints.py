from enum import Enum


class GameSizeParameters(Enum):
    """
    Enum for the min/max length of each parameter of the game board.
    This is due to avoid the UI looking stupid
    """
    min_rows = 3
    max_rows = 20
    min_cols = 3
    max_cols = 20
    min_win_length = 3
    # Max win length is forced by other parameters

    default_rows = 3
    default_cols = 3
    default_win_length = 3
