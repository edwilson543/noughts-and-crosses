"""
Module containing constant values used in the backend application.
Note that these values should not be changed.
"""


# Standard library imports
from enum import Enum


class BoardMarking(Enum):
    """
    Enum for the different options to enter on the Noughts and Crosses playing_grid.
    The reason for marking an EMPTY cell with 1j is so that when a row/column/diagonal is convoluted with a ones array
    of the winning streak length, we know whether or not the streak can be completed by checking that:
    abs(real part) + abs(imaginary part) = winning length
    """
    X = 1
    O = -1
    EMPTY = 1j


class StartingPlayer(Enum):
    """
    Enum for the different options of who starts the game.
    Note the X and O values match the BoardMarking above.
    """
    PLAYER_X = 1
    RANDOM = 0
    PLAYER_O = -1
