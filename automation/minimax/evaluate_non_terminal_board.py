"""
Module to define how the board should be scored from the maximiser's perspective when
the board is not terminal.
With the introduction of iterative deepening and a time out, the vast majority of calls end in
an early evaluation (i.e. a non-terminal board), and so a scoring system is needed that indicates how favourable
a board is for later in the game.

This could ultimately use a transposition table derived from previous games.
"""

# Standard library imports
from typing import Tuple, List, Set

# Third party imports
import numpy as np

# Local application imports
from game.app.win_check_cache_decorators import LRUCacheWinSearch
from game.app.game_base_class import NoughtsAndCrosses
from game.constants.game_constants import BoardMarking


# @LRUCacheWinSearch(hash_key_kwargs={"playing_grid", "get_win_location"}, maxsize=1000000, use_symmetry=True)
def evaluate_non_terminal_board(playing_grid: np.ndarray,
                                win_length_k: int,
                                player_turn_value: BoardMarking) -> int:
    """
    Method to determine the score that should be assigned to a board, from the perspective of the maximising player who
    is here assumed to be the player who's turn it is.
    The idea is to identify any streaks of significant length and assign a score to these. For example, if we find
    a board

    Parameters:
    ----------
    playing_grid - the board we are searching for a win
    win_length - the length of winning streak in the active game. This is used to determine the favourability of certain
    configurations.
    player_turn_value - the player who's turn it is in the game - if the board is configured favourably for the player_turn_value
    then a high score is returned, vice-versa, a low score is returned
    """
    array_list = NoughtsAndCrosses.get_non_empty_array_list(playing_grid=playing_grid, win_length_k=win_length_k)
    total_score = sum(_score_individual_array(array=array, win_length_k=win_length_k,
                                              player_turn_value=player_turn_value) for array in array_list)
    return total_score


def _score_individual_array(array: np.ndarray, win_length_k: int, player_turn_value: BoardMarking):
    """
    Method to determine the score to be associated with an individual array.
    We convolve with a ones array of length _win_length_k - this gives an idea of whether an incomplete streak
    could be completed, noting that (1, 1, 1) . (1, 1, 0) = 2, where as (1, 1, 1) . (1, 1, -1) = 1.

    This is not perfect but gives some indication.
    """
    convolved_array = np.convolve(array, np.ones(win_length_k, dtype=int), mode="valid")
    convolved_array_active_player = convolved_array * player_turn_value  # Now a high +ve score is good for the active
    # player and a low -ve score is bad, because player turn value is 1 or -1

    scores_active_player = np.sum(convolved_array_active_player ** 3)
    # Cubed to reflect the non-linear increase in favourability of a streak of longer length, and squaring loses sign
    return scores_active_player
