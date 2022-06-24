"""
Module to define how the board should be scored from the maximiser's perspective when the board is not terminal.
With the introduction of iterative deepening and a time out, the majority of calls end in an evaluation of a non-
terminal board, and so a scoring system is needed that indicates how favourable a non-terminal board is.

This could use a transposition table derived from previous games, for opening moves, but is calculated on the fly for
now.
"""

# Standard library imports
from typing import List

# Third party imports
import numpy as np

# Local application imports
from automation.minimax.constants.terminal_board_scores import TerminalScore
from game.app.game_base_class import NoughtsAndCrosses
from game.constants.game_constants import BoardMarking
from utils import lru_cache_hashable


@lru_cache_hashable(maxsize=1000000)
def evaluate_non_terminal_board(playing_grid: np.ndarray,
                                win_length_k: int,
                                search_depth: int,
                                player_turn_value: BoardMarking) -> int:
    """
    Method to determine the streak that should be assigned to a board, from the perspective of the maximising player.
    The idea is to identify any streaks of significant length and assign a streak to these.

    Parameters:
    ----------
    playing_grid - the board we are scoring
    win_length_k - the length of a winning streak in the active game. This is used to determine the favourability of
    different configurations.
    search_depth - The search depth at which the board we are scoring has been generated.
    player_turn_value - the player who has JUST MADE THEIR MOVE in the game
    i.e. the player from who's perspective we are scoring the board. If the board is favourable to that player,
    then a high (positive) streak is returned, else a low (negative) streak is returned.
    """
    # Get a list of the streaks (convolutions of each part of the board of length win_length_k with a ones array)
    array_list = NoughtsAndCrosses.get_non_empty_array_list(playing_grid=playing_grid, win_length_k=win_length_k)
    streak_list: List[np.ndarray[complex]] = [_get_convolved_array(array=array, win_length_k=win_length_k,
                                                                   player_turn_value=player_turn_value) for array in
                                              array_list]
    all_streaks: np.ndarray[complex] = np.hstack(streak_list)
    real_streaks: np.ndarray[int] = np.real(all_streaks)

    # Check who currently has a longer streak - this informs the scoring strategy
    max_player_max_streak = abs(max(real_streaks))  # maximiser player's streaks are positive
    min_player_max_streak = abs(min(real_streaks))  # minimiser player's streaks are negative
    maximiser_leading = max_player_max_streak > min_player_max_streak

    # Add up the scores of each individual streak and penalise with search depth
    total_score = np.sum(_score_individual_streak(streak=streak, win_length_k=win_length_k,
                                                  maximiser_leading=maximiser_leading) for streak in all_streaks)
    if total_score > 0:
        return max(total_score - search_depth, 0)
    else:
        return min(total_score + search_depth, 0)


def _score_individual_streak(streak: complex, win_length_k: int, maximiser_leading: bool) -> float:
    """
    Method to assign a score to an individual streak

    Score e.g.s:
    """
    real_part = streak.real
    imag_part = streak.imag
    if abs(real_part) + abs(imag_part) < win_length_k:
        # No streak can be achieved, because the number of empty cells is insufficient to complete a streak
        return 0
    elif real_part == -(win_length_k - 1):
        return TerminalScore.ONE_MOVE_FROM_LOSS.value
    elif (real_part == win_length_k - 1) and maximiser_leading:
        return TerminalScore.ONE_FROM_WIN_MAXIMISER_LEADING.value
    elif (win_length_k > 3) and (not maximiser_leading) and (real_part == -(win_length_k - 2)):
        return TerminalScore.TWO_MOVES_FROM_LOSS.value
    else:
        return real_part ** 3


def _get_convolved_array(array: np.ndarray, win_length_k: int, player_turn_value: BoardMarking):
    """
    Method to determine the streak to be associated with an individual array.
    We convolve with a ones array of length win_length_k - this gives an idea of whether an incomplete streak
    could be completed, noting that (1, 1, 1) . (1, 1, 0) = 2, where as (1, 1, 1) . (1, 1, -1) = 1.

    Parameters:
    __________
    array - the individual array that we are scoring (a row, column, diagonal etc.)
    win_length_k/player_turn_value - as above.

    Note that the scoring mechanism is clearly not perfect but gives some indication of a favourable board.
    """
    # ##########
    # # TODO delete once replaced board 0s with is
    # complex_array = np.where(array == 0, 1j, array)
    # ##########

    convolved_array = np.convolve(array, np.ones(win_length_k, dtype=int), mode="valid")
    convolved_array_active_player = convolved_array * player_turn_value  # Now a +ve streak is good for the active
    # player and a -ve streak is bad, because player turn value is 1 or -1

    return convolved_array_active_player
