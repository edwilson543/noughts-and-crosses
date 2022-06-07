"""
Module for testing the 2 search algorithms in the Noughts and Crosses base class.
One of these is a while board search, the other only searches the intersection of the board with the last turn.
"""

from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking
import pytest
import numpy as np


@pytest.fixture(scope="function")
def empty_game_parameters():
    """
    Note that the starting_player_value is normally overridden during tests.
    "Empty game" because the playing grid is empty, i.e. only contains zeros.
    """
    return NoughtsAndCrossesEssentialParameters(
        game_rows_m=5,
        game_cols_n=4,
        win_length_k=3,
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def empty_game(empty_game_parameters):
    return NoughtsAndCrosses(setup_parameters=empty_game_parameters)


class TestNoughtsAndCrossesWinCheckAndSearchLocationFiveFour:
    """
    Test class purely for testing the win search location algorithm of the NoughtsAndCrosses class.
    All tests in this class test both the win bool value and win locations return.
    """
    def test_horizontal_win_top_right_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 1, 1],
            [0, -1, 0, -1],
            [0, -1, 0, 1],
            [0, 0, 0, 1],
            [1, -1, 1, -1]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([0, 3]), get_win_location=True)
        expected_win_location = {(0, 1), (0, 2), (0, 3)}
        assert win and (set(win_locations) == expected_win_location)

    def test_horizontal_win_middle_left_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, -1],
            [-1, -1, -1, 1],
            [0, 0, 0, -1],
            [1, -1, 1, -1]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([2, 1]), get_win_location=True)
        expected_win_location = {(2, 0), (2, 1), (2, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_middle_left_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1],
            [-1, -1, 1, 1],
            [-1, 1, -1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([2, 0]), get_win_location=True)
        expected_win_location = {(1, 0), (2, 0), (3, 0)}
        assert win and (set(win_locations) == expected_win_location)

    def test_vertical_win_middle_top_right(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 1, -1],
            [-1, 0, 1, 1],
            [-1, -1, 1, -1],
            [1, -1, -1, 0],
            [0, 0, 0, 0]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([0, 2]), get_win_location=True)
        expected_win_location = {(0, 2), (1, 2), (2, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 0, 0],
            [-1, 1, 0, 0],
            [0, -1, 1, 0],
            [-1, 0, 0, 1],
            [1, -1, 0, 0]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([3, 3]), get_win_location=True)
        expected_win_location = {(1, 1), (2, 2), (3, 3)}
        assert win and (set(win_locations) == expected_win_location)

    def test_south_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 1, 0],
            [-1, -1, 0, 0],
            [0, -1, -1, 0]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([3, 1]), get_win_location=True)
        expected_win_location = {(2, 0), (3, 1), (4, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Tests for north east diagonal win
    ##########
    def test_south_west_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 0, 0],
            [0, 0, 1, -1],
            [1, 0, -1, 0],
            [0, -1, 0, -1],
            [0, 0, -1, 0]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([1, 3]), get_win_location=True)
        expected_win_location = {(1, 3), (2, 2), (3, 1)}
        assert win and (set(win_locations) == expected_win_location)

    def test_south_west_win_upper_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 1, 0],
            [0, 1, 0, -1],
            [1, 0, -1, -1],
            [-1, -1, 0, 0],
            [1, -1, 1, -1]
        ])
        win, win_locations = empty_game.win_check_and_location_search(
            last_played_index=np.array([1, 1]), get_win_location=True)
        expected_win_location = {(0, 2), (1, 1), (2, 0)}
        assert win and (set(win_locations) == expected_win_location)


class TestNoughtsAndCrossesWinCheckOnlyFiveFour:
    """
    Test class purely for testing the win search location algorithm of the NoughtsAndCrosses class.
    All tests in this class test both the win bool value and win locations return.
    """
    def test_horizontal_win_top_right_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 1, 1],
            [0, -1, 0, -1],
            [0, -1, 0, 1],
            [0, 0, 0, 1],
            [1, -1, 1, -1]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([0, 2]), get_win_location=False)
        expected_win_location = [(0, 1), (0, 2), (0, 3)]
        assert win

    def test_horizontal_win_middle_left_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, -1],
            [-1, -1, -1, 1],
            [0, 0, 0, -1],
            [1, -1, 1, -1]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([2, 1]), get_win_location=False)
        expected_win_location = [(2, 0), (2, 1), (2, 2)]
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_middle_left_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1],
            [-1, -1, 1, 1],
            [-1, 1, -1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([2, 0]), get_win_location=False)
        expected_win_location = [(1, 0), (2, 0), (3, 0)]
        assert win

    def test_vertical_win_middle_top_right(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 1, -1],
            [-1, 0, 1, 1],
            [-1, -1, 1, -1],
            [1, -1, -1, 0],
            [0, 0, 0, 0]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([0,2]), get_win_location=False)
        expected_win_location = [(0, 2), (1, 2), (2, 2)]
        assert win

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 0, 0],
            [-1, 1, 0, 0],
            [0, -1, 1, 0],
            [-1, 0, 0, 1],
            [1, -1, 0, 0]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([3, 3]), get_win_location=False)
        expected_win_location = [(1, 1), (2, 2), (3, 3)]
        assert win

    def test_south_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 1, 0],
            [-1, -1, 0, 0],
            [0, -1, -1, 0]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([3, 1]), get_win_location=False)
        expected_win_location = [(2, 0), (3, 1), (4, 2)]
        assert win

    ##########
    # Tests for north east diagonal win
    ##########
    def test_south_west_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 0, 0],
            [0, 0, 1, -1],
            [1, 0, -1, 0],
            [0, -1, 0, -1],
            [0, 0, -1, 0]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([1, 3]), get_win_location=False)
        expected_win_location = [(1, 3), (2, 2), (3, 1)]
        assert win

    def test_south_west_win_upper_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 1, 0],
            [0, 1, 0, -1],
            [1, 0, -1, -1],
            [-1, -1, 0, 0],
            [1, -1, 1, -1]
        ])
        win, _ = empty_game.win_check_and_location_search(
            last_played_index=np.array([1, 1]), get_win_location=False)
        expected_win_location = [(0, 2), (1, 1), (2, 0)]
        assert win


class TestNoughtsAndCrossesWinCheckOnlyFourThree:
    """
    Test class purely for testing the win check algorithm, for a four three game
    """
    @pytest.fixture(scope="class")
    def four_three_game_parameters(self):
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=4,
            game_cols_n=3,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def four_three_game(self, empty_game_parameters):
        return NoughtsAndCrosses(setup_parameters=empty_game_parameters)

    ##########
    # Checks playing_grid is not a winner
    ##########
    def test_no_win_full_board(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([0, 0]), get_win_location=False)
        assert not win

    def test_no_win_empty_board(self, four_three_game):
        four_three_game.playing_grid = np.zeros(shape=(4, 3))
        four_three_game.playing_grid[1, 1] = BoardMarking.X.value
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([1, 1]),get_win_location=False)
        assert not win

    ##########
    # Test for horizontal wins
    ##########
    def test_horizontal_win_top(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, 1, 1],
            [-1, 0, -1],
            [0, -1, 0],
            [0, 0, 0]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([0, 1]), get_win_location=False)
        assert win

    def test_horizontal_win_middle(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([2, 2]), get_win_location=False)
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_win_bottom_left(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([3, 0]), get_win_location=False)
        assert win

    def test_vertical_win_top_right(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([1, 2]), get_win_location=False)
        assert win

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [-1, 1, 0],
            [0, -1, 1],
            [-1, 0, -1],
            [1, -1, 0]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([1, 1]), get_win_location=False)
        assert win

    def test_south_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([3, 2]), get_win_location=False)
        assert win

    ##########
    # Tests for north east diagonal win
    ##########

    def test_north_east_win_leading_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, -1],
            [1, -1, 0],
            [-1, 0, -1],
            [0, -1, 0]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([2, 0]), get_win_location=False)
        assert win

    def test_north_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        win, _ = four_three_game.win_check_and_location_search(
            last_played_index=np.array([2, 1]), get_win_location=False)
        assert win


##########
# This is a whole board search, i.e. is naive to where the last move was played
##########

class TestNoughtsAndCrossesWholeBoardSearchAlgorithm:
    """
    Test class for the OLD search algorithm of the NoughtsAndCrosses class (_winning_board_search)
    (Chiefly its component methods)
    """
    @pytest.fixture(scope="class")
    def empty_game_parameters(self):
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=4,
            game_cols_n=3,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def empty_game(self, empty_game_parameters):
        return NoughtsAndCrosses(setup_parameters=empty_game_parameters)

    ##########
    # Checks playing_grid is not a winner
    ##########
    def test_no_win_full_board(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1]
        ])
        win = empty_game._whole_board_search()
        assert not win

    def test_no_win_empty_board(self, empty_game):
        empty_game.playing_grid = np.zeros(shape=(4, 3))
        win = empty_game._whole_board_search()
        assert not win

    ##########
    # Test for horizontal wins
    ##########
    def test_horizontal_win_top(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 1, 1],
            [-1, 0, -1],
            [0, -1, 0],
            [0, 0, 0]
        ])
        win = empty_game._whole_board_search()
        assert win

    def test_horizontal_win_middle(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        win = empty_game._whole_board_search()
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_win_bottom_left(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]
        ])
        win = empty_game._whole_board_search()
        assert win

    def test_vertical_win_top_right(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        win = empty_game._whole_board_search()
        assert win

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 0],
            [0, -1, 1],
            [-1, 0, -1],
            [1, -1, 0]
        ])
        win = empty_game._whole_board_search()
        assert win

    def test_south_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        win = empty_game._whole_board_search()
        assert win

    ##########
    # Tests for north east diagonal win
    ##########

    def test_north_east_win_leading_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, -1],
            [1, -1, 0],
            [-1, 0, -1],
            [0, -1, 0]
        ])
        win = empty_game._whole_board_search()
        assert win

    def test_north_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        win = empty_game._whole_board_search()
        assert win

    ##########
    # Tests to see output of decomposing diagonals
    ##########
    def test_south_east_diagonal_list(self, empty_game):
        """Tests whether the get_south_east_diagonal_list method is working"""
        empty_game.game_rows_m = 5
        empty_game.game_cols_n = 6
        empty_game.playing_grid = np.arange(30).reshape((5, 6))
        # Using a set to avoid list order failing the test (which is irrelevant):
        expected_diagonal_arrays = [
            np.array([3, 10, 17]),
            np.array([2, 9, 16, 23]),
            np.array([1, 8, 15, 22, 29]),
            np.array([0, 7, 14, 21, 28]),
            np.array([6, 13, 20, 27]),
            np.array([12, 19, 26])
            ]
        actual_diagonal_arrays: list = empty_game._get_south_east_diagonal_arrays(playing_grid=empty_game.playing_grid)
        for act_array in actual_diagonal_arrays:
            validity = False
            for exp_array in expected_diagonal_arrays:
                validity += np.all(act_array == exp_array)
            assert validity

    def test_north_west_diagonal_list(self, empty_game):
        """Tests whether the get_south_east_diagonal_list method is working"""
        empty_game.game_rows_m = 5
        empty_game.game_cols_n = 6
        empty_game.playing_grid = np.arange(30).reshape((5, 6))
        # Using a set to avoid list order failing the test (which is irrelevant):
        expected_diagonal_arrays = [
            np.array([12, 7, 2]),
            np.array([18, 13, 8, 3]),
            np.array([24, 19, 14, 9, 4]),
            np.array([25, 20, 15, 10, 5]),
            np.array([26, 21, 16, 11]),
            np.array([27, 22, 17])
            ]
        actual_diagonal_arrays: list = empty_game._get_north_east_diagonal_arrays()
        for act_array in actual_diagonal_arrays:
            validity = False
            for exp_array in expected_diagonal_arrays:
                validity += np.all(act_array == exp_array)
            assert validity
