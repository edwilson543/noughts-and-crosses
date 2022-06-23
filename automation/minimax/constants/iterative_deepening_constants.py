"""Module to define the constants used in the minimax algorithm for implementing iterative deepening."""

# Standard library imports
from enum import Enum


class IterativeDeepening(Enum):
    """
    Enum defining the parameters necessary to implement iterative deepening.
    Note that the max_branch_factor is included because otherwise in larger games we just run out of time searching
    every cell at search depth 1, 2, ... and n
    """
    max_search_depth = 10  # Note 0 is counted as the first search depth
    max_search_seconds = 2

    @staticmethod
    def get_max_branch_factor(search_depth: int):
        """
        Method that returns a maximum branch factor when minimax is searching at different depths.
        A max branch factor is included so that in larger games minimax doesn't just run out of time searching every
        cell at search depth 1, 2, ... and never reaching greater depth.

        There is effectively no max branch factor at search depth 0, so that minimax never leaves the board in a state
        where the other play can win immediately.
        At search depths greater than 0, we just search the 3x3 square around the last played index, as this is the
        only part of the board that has changed since moving on from search_depth 0
        """
        if search_depth == 0:
            return 961
        else:
            return 8
