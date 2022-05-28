from enum import Enum


class GameParameterConstraint(Enum):
    """
    Enum for the min/max length of each parameter of the game board.
    This is to avoid the UI looking stupid.
    """
    # Game structural setup_parameters
    min_rows = 3
    max_rows = 20
    min_cols = 3
    max_cols = 20
    min_win_length = 3
    # Note that max win length is forced by other setup_parameters

    default_rows = 3
    default_cols = 3
    default_win_length = 3


class PlayerNameConstraint(Enum):
    """Enum restricting the length of player names"""
    min_name_length = 1
    max_name_length = 8
