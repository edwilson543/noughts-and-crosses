"""Module to define the constants used in the minimax algorithm for implementing iterative deepening."""

# Standard library imports
from enum import Enum


class IterativeDeepening(Enum):
    """Enum defining the parameters necessary to implement iterative deepening."""
    max_search_depth = 5
    max_search_seconds = 100
