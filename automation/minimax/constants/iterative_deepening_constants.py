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

    @staticmethod
    def get_max_branch_factor(search_depth: int):
        """Method that returns a maximum branch factor when minimax is searching at different depths"""
        if search_depth == 0:
            return 1000000  # essentially no max branch factor
        else:
            return 24  # 5x5 grid around the last played index
