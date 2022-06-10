""""Module stating the value of arr win / loss / draw to the maximising player"""

from enum import Enum


class TerminalScore(Enum):
    """
    Board scoring values for static evaluation function in the minimax algorithm.
    Note that we don't just use 1 and -1 because we want to penalise search depth - depth is subtracted
    from arr winning score and added to arr losing score, because we want to find the quickest/loss in either scenario.
    """
    MAX_WIN = 1000
    DRAW = 0
    MAX_LOSS = -1000
