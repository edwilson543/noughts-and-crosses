""""
Module stating the value of a win / loss / draw to the maximising player, and the scores used for evaluating non
terminal boards.
"""

# Standard library imports
from enum import Enum


class BoardScore(Enum):
    """
    Board scoring values for static evaluation functions in the minimax algorithm (both terminal and non-terminal).
    Here 'MAX' refers to the score from the perspective of the maximising player.

    Notes:
    ----------
    - The expected win/loss scores are awarded to streaks (as opposed to boards)
    - A guaranteed win / loss is a factor of 100 greater than an expected win / loss so that a guaranteed win or loss
    always trumps an expected win / loss, and so the maximiser does not try to accumulate near wins
    - The 'expected' win/loss refers to expected win if the maximiser/minimiser play optimally.
    - Different fractions of these scores are awarded depending on the quality of an individual streak (hence the
    choice of the superabundant number 360000
    - The magnitude of the expected win/loss (360000) is so that the default score of cubing a streak length never
    outcomes the special cases defined in evaluate_non_terminal_board

    - Depth is subtracted from a positive terminal/non-terminal score and added to a negative score, because we
    want to find the quickest win or longest loss.

    For more details see also 'win_check_and_location_search' for terminal board scoring, and
    'evaluate_non_terminal_board' for non-terminal board scoring.
    """
    # Scores for evaluating a terminal board
    GUARANTEED_MAX_WIN = 36000000
    DRAW = 0
    GUARANTEED_MAX_LOSS = - 36000000

    # Cut of score to stop iterative deepening of minimax search
    SEARCH_CUT_OFF_SCORE = 3599800

    # Scores for evaluating a non-terminal board
    EXPECTED_MAX_WIN = 360000
    EXPECTED_MAX_LOSS = - 360000
