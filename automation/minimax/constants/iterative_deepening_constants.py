"""Module to define the constants used in the minimax algorithm for implementing iterative deepening."""

# Standard library imports
from enum import Enum


class IterativeDeepening(Enum):
    """
    Enum defining the parameters necessary to implement iterative deepening.
    Note that the max_branch_factor is included because otherwise in larger games we just run out of time searching
    every cell at search depth 1, 2, ...
    """
    max_search_depth = 10  # Note 0 is counted as the first search depth
    max_search_seconds = 2
    max_branch_factor = 24  # The max number of cells to check at each depth
