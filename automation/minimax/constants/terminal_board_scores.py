""""Module stating the value of a win / loss / draw to the maximising player"""

# Standard library imports
from enum import Enum


class TerminalScore(Enum):
    """
    Board scoring values for static evaluation function in the minimax algorithm.
    Note that we don't just use 1 and -1 because we want to penalise search depth - depth is subtracted
    from a winning score and added to a losing score, because we want to find the quickest/loss in either scenario.

    Note that streaks of less than the winning length are scored by cubing the length in evaluate_non_terminal_board.
    Hence the score for a win needs to be higher than the size of a reasonable game minus one cubed:
    i.e. MAX_WIN > (max(game_rows_m, game_cols_n) - 1) ** 3, and equivalently for MAX_LOSS.

    Note that here 'MAX' refers to the score from the perspective of the maximising player.
    """
    MAX_WIN = 100000
    DRAW = 0
    MAX_LOSS = -100000
    ONE_MOVE_FROM_LOSS = - 90000  # Score for leaving the board in a state where the opposition can win in one move
    NON_TERMINAL = -5000  # TODO delete this
