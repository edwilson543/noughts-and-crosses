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
                                player_turn_value: BoardMarking,
                                maximisers_has_next_turn: bool) -> int:
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

    #TODO update NEUTRAL to who's turn it is next
    """
    # Get a list of the streaks (convolutions of each part of the board of length win_length_k with a ones array)
    array_list = NoughtsAndCrosses.get_non_empty_array_list(playing_grid=playing_grid, win_length_k=win_length_k)
    streak_list: List[np.ndarray[complex]] = [_get_convolved_array(array=array, win_length_k=win_length_k,
                                                                   player_turn_value=player_turn_value) for array in
                                              array_list]
    all_streaks: np.ndarray[complex] = np.hstack(streak_list)

    # Get rid of 'closed streaks' where there are insufficient empty cells to complete the streak
    winnable_streaks: np.ndarray[complex] = all_streaks[abs(all_streaks.real) + abs(all_streaks.imag) == win_length_k]
    relevant_streaks: np.ndarray[complex] = winnable_streaks[abs(winnable_streaks.imag) != win_length_k]
    if len(relevant_streaks) == 0:
        return 0  # Game is guaranteed to be a draw

    # Check who currently has a longer streak - this informs the scoring strategy
    real_streaks: np.ndarray[int] = np.real(relevant_streaks)
    max_player_max_streak = abs(max(real_streaks))  # maximiser player's streaks are positive
    min_player_max_streak = abs(min(real_streaks))  # minimiser player's streaks are negative
    leading_player_indicator = max_player_max_streak - min_player_max_streak

    # Add up the scores of each individual streak and penalise with search depth
    for streak in relevant_streaks:
        score = _score_individual_streak(streak=streak, win_length_k=win_length_k,
        maximiser_has_next_turn=maximisers_has_next_turn,
        leading_player_indicator=leading_player_indicator)

    total_score = sum(_score_individual_streak(
        streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=maximisers_has_next_turn,
        leading_player_indicator=leading_player_indicator) for streak in relevant_streaks)
    if total_score > 0:
        return max(total_score - search_depth, 0)
    else:
        return min(total_score + search_depth, 0)


def _score_individual_streak(streak: complex, win_length_k: int,
                             maximiser_has_next_turn: bool, leading_player_indicator: int) -> float:
    """
    Method to assign a score to an individual streak
    # TODO
    Score e.g.s:
    """
    maximiser_has_longest_streak = leading_player_indicator > 0
    maximiser_minimiser_longest_streak_same_length = leading_player_indicator == 0
    minimiser_has_longest_streak = leading_player_indicator < 0

    real_part = streak.real
    score_return = None
    if maximiser_has_next_turn:
        if real_part == win_length_k - 1:
            score_return = TerminalScore.EXPECTED_MAX_WIN.value
        elif maximiser_has_longest_streak:
            # Minimiser can't have a (win_length_k - 1) streak otherwise maximiser has won
            # Minimiser can't have a (win_length_k - 2) streak otherwise maximiser has a (win_length_k -2) streak
            if real_part == win_length_k - 2:
                # If convolution gives 2 (win_length_k - 2) streaks, this mean the maximiser has (wlk-2)-in-a-row with
                # 2 open ends - given it's maximisers turn next, they can fill one end to get a (wlk-1) streak
                score_return = TerminalScore.EXPECTED_MAX_WIN.value / 3
        elif maximiser_minimiser_longest_streak_same_length:
            # Only relevant scenario is both have a (wlk - 2) streak - in which case we score the board by who has most
            # TODO may need to make these scores different depending on who's turn it is next
            if real_part == win_length_k - 2:
                score_return = TerminalScore.EXPECTED_MAX_WIN.value / 6
            elif real_part == - (win_length_k - 2):
                score_return = - TerminalScore.DRAWING_WIN_LENGTH_MINUS_TWO.value
        elif minimiser_has_longest_streak:
            if real_part == -(win_length_k - 1):
                # Divide loss score by 2 - if minimiser has 2 (win_length_k - 1) streaks, maximiser has lost regardless
                score_return = TerminalScore.EXPECTED_MAX_LOSS.value / 2
            #  Maximiser now can't have a (wlk-2) streak, irrelevant if minimiser does as maximiser would block
            # TODO Maybe it's irrelevant what the streaks on win_length_k - 2 are - have a look
    else:  # not maximiser_has_next_turn
        if real_part == -(win_length_k - 1):
            score_return = TerminalScore.EXPECTED_MAX_LOSS.value
        elif minimiser_has_longest_streak:
            # Only option here is that minimiser has a (wlk-2) streak
            if real_part == -(win_length_k - 2):
                # If convolution gives 2 (win_length_k - 2) streaks, this means the minimiser has (wlk-2)-in-a-row with
                # 2 open ends - given it's minimiser's turn next, they can fill one end to get a (wlk-1) streak
                score_return = TerminalScore.EXPECTED_MAX_LOSS.value / 3
        elif maximiser_minimiser_longest_streak_same_length:
            # Only relevant scenario is both have a (wlk - 2) streak - in which case we score the board by who has most
            # TODO may need to make these scores different for maximiser / minimiser
            if real_part == win_length_k - 2:
                score_return = TerminalScore.DRAWING_WIN_LENGTH_MINUS_TWO.value
            elif real_part == - (win_length_k - 2):
                score_return = TerminalScore.EXPECTED_MAX_LOSS.value / 6
        elif maximiser_has_longest_streak:
            if real_part == win_length_k - 1:
                # Divide win score by 2 - if maximiser has 2 (win_length_k - 1) streaks, maximiser has won regardless
                score_return = TerminalScore.EXPECTED_MAX_WIN.value / 2
            # TODO Maybe it's irrelevant what the streaks on win_length_k - 2 are - have a look

    if score_return is None:
        score_return = real_part ** 3
    return score_return


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
    convolved_array = np.convolve(array, np.ones(win_length_k, dtype=int), mode="valid")
    convolved_array_active_player = convolved_array * player_turn_value  # Now a +ve streak is good for the active
    # player and a -ve streak is bad, because player turn value is 1 or -1

    return convolved_array_active_player
