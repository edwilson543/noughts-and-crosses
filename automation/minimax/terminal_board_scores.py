""""Module stating the value of a win / loss / draw to the maximising player"""

# Standard library imports
from enum import Enum


class TerminalScore(Enum):
    """
    Board scoring values for static evaluation function in the minimax algorithm.
    Note that we don't just use 1 and -1 because we want to penalise search depth - depth is subtracted
    from a winning score and added to a losing score, because we want to find the quickest/loss in either scenario.
    """
    MAX_WIN = 1000
    DRAW = 0
    MAX_LOSS = -1000
    NON_TERMINAL = -500
