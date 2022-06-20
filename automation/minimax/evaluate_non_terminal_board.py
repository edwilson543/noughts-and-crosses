"""
Module to define how the board should be scored from the maximiser's perspective when the board is not terminal.
With the introduction of iterative deepening and a time out, the majority of calls end in an evaluation of a non-
terminal board, and so a scoring system is needed that indicates how favourable a non-terminal board is.

This could use a transposition table derived from previous games, for opening moves, but is calculated on the fly for
now.
"""

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
    Method to determine the score that should be assigned to a board, from the perspective of the maximising player.
    The idea is to identify any streaks of significant length and assign a score to these.

    Parameters:
    ----------
    playing_grid - the board we are scoring
    win_length_k - the length of a winning streak in the active game. This is used to determine the favourability of
    different configurations.
    search_depth - The search depth at which the board we are scoring has been generated.
    player_turn_value - the player who has JUST MADE THEIR MOVE in the game
    i.e. the player from who's perspective we are scoring the board. If the board is favourable to that player,
    then a high (positive) score is returned, else a low (negative) score is returned.
    """
    array_list = NoughtsAndCrosses.get_non_empty_array_list(playing_grid=playing_grid, win_length_k=win_length_k)
    total_score = sum(_score_individual_array(array=array, win_length_k=win_length_k,
                                              player_turn_value=player_turn_value) for array in array_list)
    if total_score > 0:
        return max(total_score - search_depth, 0)
    else:
        return min(total_score + search_depth, 0)


def _score_individual_array(array: np.ndarray, win_length_k: int, player_turn_value: BoardMarking):
    """
    Method to determine the score to be associated with an individual array.
    We convolve with a ones array of length win_length_k - this gives an idea of whether an incomplete streak
    could be completed, noting that (1, 1, 1) . (1, 1, 0) = 2, where as (1, 1, 1) . (1, 1, -1) = 1.

    Parameters:
    __________
    array - the individual array that we are scoring (a row, column, diagonal etc.)
    win_length_k/player_turn_value - as above.

    Note that the scoring mechanism is clearly not perfect but gives some indication of a favourable board.
    """
    convolved_array = np.convolve(array, np.ones(win_length_k, dtype=int), mode="valid")
    convolved_array_active_player = convolved_array * player_turn_value  # Now a +ve score is good for the active
    # player and a -ve score is bad, because player turn value is 1 or -1
    if min(convolved_array_active_player) == - (win_length_k - 1):  # opposition is one away from a win
        return TerminalScore.ONE_MOVE_FROM_LOSS.value
    else:
        scores_active_player = np.sum(convolved_array_active_player ** 3)
        # Cubed to reflect the non-linear increase in favourability of a longer streak, (and squaring loses sign)
        return scores_active_player
