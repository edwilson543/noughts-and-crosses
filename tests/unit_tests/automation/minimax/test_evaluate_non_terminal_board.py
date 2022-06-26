"""Test module for the functions in the evaluate_non_terminal_board module."""

# Third party imports
import numpy as np

# Local application imports
from automation.minimax.evaluate_non_terminal_board import _get_convolved_array, evaluate_non_terminal_board, \
    _score_individual_streak
from automation.minimax.constants.terminal_board_scores import BoardScore
from game.constants.game_constants import BoardMarking


class TestEvaluateNonTerminalBoard:
    """Class for testing the evaluate_non_terminal_board method"""

    def test_maximiser_expected_to_win(self):
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, BoardMarking.EMPTY.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.O.value, BoardMarking.EMPTY.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=1, maximiser_mark_value=BoardMarking.X.value, maximiser_has_next_turn=True
        )
        assert actual_score >= BoardScore.EXPECTED_MAX_WIN.value

    def test_maximiser_expected_to_lose(self):
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, BoardMarking.EMPTY.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.O.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=3, maximiser_mark_value=BoardMarking.O.value, maximiser_has_next_turn=False
        )
        assert actual_score <= BoardScore.EXPECTED_MAX_LOSS.value

    def test_bad_to_leave_board_where_both_players_could_win(self):
        """
        Leaving the board like this isn't a very good idea - note that maximiser_mark_value corresponds to the
        player who has just been, not the player who is about to go. Whoever this is loses in this scenario.
        """
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, BoardMarking.EMPTY.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.O.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.O.value, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=2, maximiser_mark_value=BoardMarking.X.value, maximiser_has_next_turn=False,
        )
        assert actual_score <= BoardScore.EXPECTED_MAX_LOSS.value

    def test_good_to_receive_board_where_both_players_could_win(self):
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, BoardMarking.EMPTY.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.O.value],
                                 [BoardMarking.EMPTY.value, BoardMarking.O.value, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=2, maximiser_mark_value=BoardMarking.X.value, maximiser_has_next_turn=True,
        )
        assert actual_score >= BoardScore.EXPECTED_MAX_WIN.value


class TestScoreIndividualStreak:
    """
    Class for testing the _score_individual_streak function
    Note that the unit tests in this class are only intended to cover the main cases of interest.
    """

    def test_expected_to_win_if_one_from_win_at_start_of_turn(self):
        streak = 4 + 1j
        win_length_k = 5
        score = _score_individual_streak(streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=True,
                                         leading_player_indicator=1)
        assert score == BoardScore.EXPECTED_MAX_WIN.value

    def test_expected_to_lose_if_one_from_win_at_end_of_turn(self):
        """Leading player indicator = 0 signifies that maximiser also has a streak of length 4"""
        streak = - 4 + 1j
        win_length_k = 5
        score = _score_individual_streak(streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=False,
                                         leading_player_indicator=0)
        assert score == BoardScore.EXPECTED_MAX_LOSS.value

    def test_short_minimiser_streak_just_gets_cubed(self):
        """The 'short' refers to the streak not being of length (win_length_k - 1) or (win_length_k - 2)"""
        streak = - 5 + 3j
        win_length_k = 8
        score = _score_individual_streak(streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=False,
                                         leading_player_indicator=0)
        expected_score = - 125
        assert score == expected_score

    def test_short_maximiser_streak_just_gets_cubed(self):
        """The 'short' refers to the streak not being of length (win_length_k - 1) or (win_length_k - 2)"""
        streak = 5 + 3j
        win_length_k = 8
        score = _score_individual_streak(streak=streak, win_length_k=win_length_k, maximiser_has_next_turn=False,
                                         leading_player_indicator=0)
        expected_score = 125
        assert score == expected_score


class TestGetConvolvedArray:
    """Class for testing the _get_convolved_array function"""

    def test_get_convolved_array_empty_row(self):
        win_length_k = 5
        maximiser_mark_value = BoardMarking.X.value
        board_row = np.array([BoardMarking.EMPTY.value] * 6)

        expected_convolution = np.array([5j, 5j])
        actual_convolution = _get_convolved_array(array=board_row, win_length_k=win_length_k,
                                                  maximiser_mark_value=maximiser_mark_value)

        assert np.all(expected_convolution == actual_convolution)

    def test_get_convolved_array_streaks_positive_for_maximiser_x(self):
        """
        Test that the real part of the streaks in the convolved arrays is positive when the streak belongs
        to the maximiser, when the maximiser is playing as x.
        (Note that the streaks are not winnable so would get filtered out anyway)
        """
        win_length_k = 5
        maximiser_mark_value = BoardMarking.X.value
        board_row = np.array([BoardMarking.X.value, BoardMarking.X.value, BoardMarking.X.value, BoardMarking.O.value,
                              BoardMarking.EMPTY.value, BoardMarking.X.value])

        expected_convolution = np.array([2 + 1j, 2 + 1j])
        actual_convolution = _get_convolved_array(array=board_row, win_length_k=win_length_k,
                                                  maximiser_mark_value=maximiser_mark_value)

        assert np.all(expected_convolution == actual_convolution)

    def test_get_convolved_array_streaks_positive_for_maximiser_o(self):
        """
        Test that the real part of the streaks in the convolved arrays is positive when the streaks belong
        to the maximiser, when the maximiser is playing as x.
        (Note that the streaks are not winnable so would get filtered out anyway)
        """
        win_length_k = 5
        maximiser_mark_value = BoardMarking.O.value
        board_row = np.array([BoardMarking.O.value, BoardMarking.O.value, BoardMarking.O.value, BoardMarking.X.value,
                              BoardMarking.EMPTY.value, BoardMarking.O.value])

        expected_convolution = np.array([-2 - 1j, -2 - 1j])
        actual_convolution = _get_convolved_array(array=board_row, win_length_k=win_length_k,
                                                  maximiser_mark_value=maximiser_mark_value)

        assert np.all(expected_convolution == actual_convolution)

    def test_get_convolved_array_streaks_negative_for_maximiser_x(self):
        """
        Test that the real part of the streaks in the convolved arrays is negative when the streaks belong
        to the minimiser, when the maximiser is playing as x.
        (Note that the streaks are not winnable so would get filtered out anyway)
        """
        win_length_k = 5
        maximiser_mark_value = BoardMarking.X.value
        board_row = np.array([BoardMarking.O.value, BoardMarking.O.value, BoardMarking.O.value, BoardMarking.X.value,
                              BoardMarking.EMPTY.value, BoardMarking.O.value])

        expected_convolution = np.array([-2 + 1j, -2 + 1j])
        actual_convolution = _get_convolved_array(array=board_row, win_length_k=win_length_k,
                                                  maximiser_mark_value=maximiser_mark_value)

        assert np.all(expected_convolution == actual_convolution)

    def test_get_convolved_array_streaks_negative_for_maximiser_o(self):
        """
        Test that the real part of the streaks in the convolved arrays is negative when the streaks belong
        to the minimiser, when the maximiser is playing as o.
        (Note that the streaks are not winnable so would get filtered out anyway)
        """
        win_length_k = 5
        maximiser_mark_value = BoardMarking.O.value
        board_row = np.array([BoardMarking.X.value, BoardMarking.X.value, BoardMarking.X.value, BoardMarking.O.value,
                              BoardMarking.EMPTY.value, BoardMarking.X.value])

        expected_convolution = np.array([-2 - 1j, -2 - 1j])
        actual_convolution = _get_convolved_array(array=board_row, win_length_k=win_length_k,
                                                  maximiser_mark_value=maximiser_mark_value)

        assert np.all(expected_convolution == actual_convolution)
