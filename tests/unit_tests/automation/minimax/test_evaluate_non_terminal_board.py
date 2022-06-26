"""Test module for the functions in the evaluate_non_terminal_board module."""

# Standard library imports
import pytest

# Third party imports
import numpy as np

# Local application imports
from automation.minimax.evaluate_non_terminal_board import _get_convolved_array, evaluate_non_terminal_board
from automation.minimax.constants.terminal_board_scores import BoardScore
from game.constants.game_constants import BoardMarking

# TODO write tests for these methods

@pytest.mark.skip(reason="Methods not fully defined yet")
class TestEvaluateNonTerminalBoard:
    def test_score_quite_good_for_player_x(self):
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, 0],
                                 [0, BoardMarking.O.value, 0],
                                 [0, 0, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=1, player_turn_value=BoardMarking.X.value
        )
        expected_score = 4 - 1  # (8 + 1 - 1 - 1 - 1 - 1 - 1) - search_depth
        assert actual_score == expected_score

    def test_score_quite_bad_for_player_o(self):
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, 0],
                                 [0, BoardMarking.O.value, 0],
                                 [0, 0, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=3, player_turn_value=BoardMarking.O.value
        )
        expected_score = BoardScore.ONE_MOVE_FROM_LOSS.value
        assert actual_score == expected_score

    def test_score_symmetric_board_both_players_could_win(self):
        """
        Leaving the board like this isn't a very good idea - note that player_turn_value corresponds to the
        player who has just been, not the player who is about to go. Whoever this is loses in this scenario.
        """
        playing_grid = np.array([[BoardMarking.X.value, BoardMarking.X.value, 0],
                                [BoardMarking.X.value, 0, BoardMarking.O.value],
                                [0, BoardMarking.O.value, BoardMarking.O.value]])
        actual_score = evaluate_non_terminal_board(
            playing_grid=playing_grid, win_length_k=3,
            search_depth=2, player_turn_value=BoardMarking.X.value
        )
        expected_score = BoardScore.ONE_MOVE_FROM_LOSS.value
        assert actual_score == expected_score

@pytest.mark.skip(reason="Methods not fully defined yet")
class TestScoreIndividualArray:
    @pytest.fixture(scope="class")
    def easy_to_see_array(self):
        return np.array([BoardMarking.X.value, BoardMarking.X.value, BoardMarking.X.value, BoardMarking.X.value, 0,
                         0, 0, 0, 0, BoardMarking.O.value, BoardMarking.O.value, BoardMarking.O.value])

    def test_score_individual_array_player_x(self, easy_to_see_array):
        """
        Tests that we get the right streak - in general, that the player with the longer streak gets a +ve streak.
        Note that it can be whoever's turn, depending on what is going on elsewhere on the board.
        """
        actual_score = _get_convolved_array(
                array=easy_to_see_array,
                win_length_k=5,
                player_turn_value=BoardMarking.X.value,
            )
        expected_score = 64  # 64 + 27 + 4 + 1 + 0 +... + 0 - 1 -4 - 27
        assert actual_score == expected_score

    def test_score_individual_array_player_o(self, easy_to_see_array):
        """
        Note that we switch who's turn it is versus the below, to check that the player correctly identifies that
        a board containing this array would mean they are one move from a loss.
        """
        actual_score = _get_convolved_array(
            array=easy_to_see_array,
            win_length_k=5,
            player_turn_value=BoardMarking.O.value,
        )
        expected_score = BoardScore.ONE_MOVE_FROM_LOSS.value
        assert actual_score == expected_score
