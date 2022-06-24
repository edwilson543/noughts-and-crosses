""""Module stating the value of a win / loss / draw to the maximising player"""

# Standard library imports
from enum import Enum


class TerminalScore(Enum):
    """
    Board scoring values for static evaluation functions in the minimax algorithm (both terminal and non-terminal).
    Note that we don't just use 1 and -1 because we want to penalise search depth, and also account for the non terminal
    board scoring system - depth is subtracted from a winning streak and added to a losing streak, because we want to
    find the quickest win or longest loss.

    Note that streaks of less than the winning length are scored according to different criteria in the
    evaluate_non_terminal_board method.
    The default is to cubed the length of an open streak in, hence the score for a win needs to be higher than the size
    of a reasonable game's dimensions.
    i.e. MAX_WIN > (max(game_rows_m, game_cols_n) - 1) ** 3, and equivalently for MAX_LOSS.

    Here 'MAX' refers to the score from the perspective of the maximising player.

    See also 'win_check_and_location_search' for terminal board scoring, and 'evaluate_non_terminal_board' for non-
    terminal board scoring.
    """
    # Scores for evaluating a terminal board
    MAX_WIN = 100000
    DRAW = 0
    MAX_LOSS = -100000

    # Scores for evaluating a non-terminal board
    ONE_MOVE_FROM_LOSS = - 5000  # Score for leaving the board in a state where the opposition can win in one move
    TWO_MOVES_FROM_LOSS = - 2000  # Only deducted if maximiser is not leading (but streaks may be level)
    ONE_FROM_WIN_MAXIMISER_LEADING = 1000  # Only awarded if minimiser doesn't have a streak of win_length_k - 1
    CUT_OFF_SCORE_TO_STOP_SEARCHING = 1000  # Stop iterative deepening search once this is achieved
