"""Module to define the constants used in the minimax algorithm for implementing iterative deepening."""

# Standard library imports
from enum import Enum


class IterativeDeepening(Enum):
    """Enum defining the parameters necessary to implement iterative deepening."""
    max_search_depth = 10  # Note 0 is counted as the first search depth
    max_search_seconds = 1
