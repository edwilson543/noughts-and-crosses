from enum import Enum, auto


class BoardMarking(Enum):
    """Enum for the different options to enter on the Noughts and Crosses playing_grid."""
    X = 1
    O = -1


class StartingPlayer(Enum):
    """Enum for the different options of who starts the game"""
    PLAYER_X = 1
    RANDOM = 0
    PLAYER_O = -1
