"""
Module to define how the board should be scored from the maximiser's perspective when the board is not terminal.
With the introduction of iterative deepening and a time out, the majority of calls end in an evaluation of a non-
terminal board, and so a scoring system is needed that indicates how favourable a non-terminal board is.

This could use a transposition table derived from previous games, for opening moves, but is calculated on the fly for
now.
"""

# Standard library imports
from functools import lru_cache
from typing import List

# Third party imports
import numpy as np

# Local application imports
from automation.minimax.constants.terminal_board_scores import BoardScore
from game.app.game_base_class import NoughtsAndCrosses
from game.constants.game_constants import BoardMarking
from utils import lru_cache_hashable


@lru_cache_hashable(maxsize=1000000)
def evaluate_non_terminal_board(playing_grid: np.ndarray,
                                win_length_k: int,
                                search_depth: int,
                                maximiser_mark_value: BoardMarking,
                                maximiser_has_next_turn: bool) -> int:
    """
    Method to determine the streak that should be assigned to a board, from the perspective of the maximising player.
    The overarching idea is to identify any streaks of significant length and assign a streak to these.
    We extract all rows, columns and diagonals form the playing_grid, convolve with a ones array of length win_length_k,
    score each resulting streak represented by a complex number under different scenarios, and add up the total for
    the entire playing_grid.

    Parameters:
    ----------
    playing_grid - the board we are scoring

    win_length_k - the length of a winning streak in the active game. This is used to determine the favourability of
    different configurations.

    search_depth - The search depth at which the board we are scoring has been generated.

    maximiser_mark_value - the value that represents the maximising player's board markings (1 or -1)
    i.e. the player from who's perspective we are scoring the board. If the board is favourable to that player,
    then a high (positive) streak is returned, else a low (negative) streak is returned.

    maximiser_has_next_turn - T/F depending on whether the maximiser would get to make the next move on the grid.
    """
    # Get a list of the streaks (convolutions of each part of the board of length win_length_k with a ones array)
    array_list = NoughtsAndCrosses.get_non_empty_array_list(playing_grid=playing_grid, win_length_k=win_length_k)
    streak_list: List[np.ndarray[complex]] = [_get_convolved_array(array=array, win_length_k=win_length_k,
                                                                   maximiser_mark_value=maximiser_mark_value) for array
                                              in
                                              array_list]
    all_streaks: np.ndarray[complex] = np.hstack(streak_list)

    # Get rid of closed streaks where there are insufficient empty cells to complete the streak
    winnable_streaks: np.ndarray[complex] = all_streaks[abs(all_streaks.real) + abs(all_streaks.imag) == win_length_k]
    relevant_streaks: np.ndarray[complex] = winnable_streaks[abs(winnable_streaks.imag) != win_length_k]
    if len(relevant_streaks) == 0:
        return 0  # Game is guaranteed to be a draw

    # Check who currently has a longer streak - this informs the scoring strategy
    real_streaks: np.ndarray[int] = np.real(relevant_streaks)
    max_player_max_streak = abs(max(real_streaks))  # because maximiser streaks are positive
    min_player_max_streak = abs(min(real_streaks))  # because minimiser streaks are negative
    leading_player_indicator = max_player_max_streak - min_player_max_streak

    # Add up the scores of each individual streak and penalise total with search depth
    total_score = sum(_score_individual_streak(
        streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=maximiser_has_next_turn,
        leading_player_indicator=leading_player_indicator) for streak in relevant_streaks)
    if total_score > 0:
        return max(total_score - search_depth, 0)
    else:
        return min(total_score + search_depth, 0)


@lru_cache(maxsize=1000)  # Note there are not many possibilities so can use a small cache
def _score_individual_streak(streak: complex, win_length_k: int,
                             maximiser_has_next_turn: bool, leading_player_indicator: int) -> float:
    """
    Method to assign a score to an individual streak.

    Parameters:
    ----------
    streak: The result of convoluting a win_length_k section of the playing_grid with a ones array of length
    win_length_k. Streaks are represented by complex numbers (real for the played part, imaginary for the empty part)
    Note that closed streaks which cannot be won (real + imag < win_length), as well as entirely empty streaks, are
    filtered out rather than being passed to this function.

    win_length_k: The length of a winning streak

    maximiser_has_next_turn: A boolean indicator as to whether the passed streak has come from a board on which the
    maximiser would play the next turn. False if the minimiser has the next turn.

    leading_player_indicator: The difference between the maximiser's longest streak and the minimiser's longest streak.
    The sign of this integer is used to define the scoring scenarios e.g. if > 0, then the maximiser has a longer
    streak than the minimiser, so the scoring of such streaks is more favourable. This is essential to the scoring,
    because if the minimiser is one move from a win, then the maximiser should not be rewarded for making a move which
    also makes them one move from a win...

    Explanation of the scoring system:
    ----------
    We consider the main scenarios to be the cartesian product of the leading_player_indicator signs (>0, ==0, <0)
    and T/F for maximiser_has_next_turn (giving 6 scenarios in total).

    In each scenario, as relevant, a score is assigned to the maximiser/ minimiser having a streak of length one- and
    two-off a winning streak. Scores are assigned as a portion of EXPECTED_MAX_WIN and EXPECTED_MAX_LOSS to reflect
    the relative benefit of the given streak under each of the scenarios.

    Note that the scoring system is largely symmetric (i.e. if maximiser has next turn and has a streak of
    win_length_k - 1, then the full EXPECTED_MAX_WIN is awarded, while if the minimiser has the next turn and has a
    streak of length win_length_k - 1 then the full EXPECTED_MAX_LOSS is awarded)

    See commentary throughout code for explaining the scoring within each scenario.
    """
    maximiser_has_longest_streak = leading_player_indicator > 0
    maximiser_minimiser_longest_streak_same_length = leading_player_indicator == 0
    minimiser_has_longest_streak = leading_player_indicator < 0

    streak_length = streak.real
    score_return = None
    if maximiser_has_next_turn:
        if streak_length == win_length_k - 1:
            score_return = BoardScore.EXPECTED_MAX_WIN.value
        elif maximiser_has_longest_streak:
            # Minimiser can't have a (win_length_k - 1) streak otherwise maximiser has won
            # Minimiser can't have a (win_length_k - 2) streak otherwise maximiser has a (win_length_k -2) streak
            if streak_length == win_length_k - 2:
                # If convolution gives 3 (win_length_k - 2) streaks, this (could) mean the maximiser has (wlk-2) with
                # 2 open ends - given it's maximisers turn next, they can fill one end to get a (wlk-1) streak
                score_return = BoardScore.EXPECTED_MAX_WIN.value / 3
        elif maximiser_minimiser_longest_streak_same_length:
            # Only possible scenario is both have a (wlk - 2) streak - in which case we score the board such that a
            # (wlk - 2) streak is more favourable to the player who's turn is next
            # Note that /6 and /9 have been carefully chosen to reflect competition with the other streak's scores
            if streak_length == win_length_k - 2:
                score_return = BoardScore.EXPECTED_MAX_WIN.value / 6
            elif streak_length == - (win_length_k - 2):
                score_return = BoardScore.EXPECTED_MAX_LOSS.value / 9
        elif minimiser_has_longest_streak:
            #  Maximiser can't have a (wlk-2) streak, irrelevant if minimiser does as maximiser would block
            if streak_length == -(win_length_k - 1):
                # Divide loss score by 2 - if minimiser has 2 (win_length_k - 1) streaks, maximiser has lost regardless
                score_return = BoardScore.EXPECTED_MAX_LOSS.value / 2
    else:  # not maximiser_has_next_turn
        if streak_length == -(win_length_k - 1):
            score_return = BoardScore.EXPECTED_MAX_LOSS.value
        elif minimiser_has_longest_streak:
            # Only possible, relevant scenario here is that minimiser has a (wlk-2) streak
            if streak_length == -(win_length_k - 2):
                # If convolution gives 3 (win_length_k - 2) streaks, this (could) mean the minimiser has (wlk-2) with
                # 2 open ends - given it's minimiser's turn next, they can fill one end to get a (wlk-1) streak
                score_return = BoardScore.EXPECTED_MAX_LOSS.value / 3
        elif maximiser_minimiser_longest_streak_same_length:
            # Only possible scenario is both have a (wlk - 2) streak - in which case we score the board such that a
            # (wlk - 2) streak is more favourable to the player who's turn is next
            if streak_length == win_length_k - 2:
                score_return = BoardScore.EXPECTED_MAX_WIN.value / 9
            elif streak_length == - (win_length_k - 2):
                score_return = BoardScore.EXPECTED_MAX_LOSS.value / 6
        elif maximiser_has_longest_streak:
            if streak_length == win_length_k - 1:
                # Divide win score by 2 - if maximiser has 2 (win_length_k - 1) streaks, maximiser has won regardless
                score_return = BoardScore.EXPECTED_MAX_WIN.value / 2

    if score_return is None:
        # Streak does not fall into any of the above scenarios, so just cube it (which retains the sign)
        score_return = streak_length ** 3
    return score_return


def _get_convolved_array(array: np.ndarray, win_length_k: int,
                         maximiser_mark_value: BoardMarking) -> np.ndarray:
    """
    Method to determine the streak complex number to be associated with an individual array.
    We convolve with a ones array of length win_length_k - this tells us whether an incomplete streak could be
    completed.
    We also multiply by the player turn value, so that a positive streak is good for the maximiser, and a negative
    streak is bad, noting that for a streak = -3, this is good for player represented by -1, and bad for player
    represented by 1, so multiplying -1 * -3 tells us that this is a good streak for the maximiser_mark_value.

    Parameters:
    __________
    array - the individual array that we are scoring (a row, column, diagonal etc. of the playing grid)
    win_length_k/maximiser_mark_value - as above.

    Returns:
    ----------
    A numpy array containing the complex numbers that represent the streaks.
    The length of the output array will be: len(array) - win_length_k + 1

    Examples:
    (1, 1, 1) . (1, 1, j) = 2 + j  ---> This streak could be completed as real + imag part equal win_length (of 3)
    (1, 1, 1) . (1, 1, -1) = 1     ---> This streak would get filtered out (i.e. not scored) as it can't be won
    (1, -1, j) . (1, 1, 1) = j     ---> This streak would get filtered out (i.e. not scored) as it can't be won
    """
    convolved_array = np.convolve(array, np.ones(win_length_k, dtype=int), mode="valid")
    convolved_array_active_player = convolved_array * maximiser_mark_value  # Now a +ve streak is good for the maximiser
    # and a -ve streak is bad, because player turn value is 1 or -1

    return convolved_array_active_player
