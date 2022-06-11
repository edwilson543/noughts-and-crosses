"""Module listing the constant column header names used when collecting game simulation data"""

# Standard library imports
from enum import Enum, auto


class PlayerOptions(Enum):
    """Enumeration of the different player options the simulated players can be."""
    MINIMAX = auto()
    RANDOM = auto()


class SimulationColumnName(Enum):
    """Enumeration of the different column names to be used in the dataframe collection game simulation data"""
    STARTING_PLAYER = auto()
    WINNING_PLAYER = auto()
    BOARD_STATUS = auto()
    MOVE = auto()
