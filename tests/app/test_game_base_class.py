from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, WinOrientation
import pytest
import numpy as np
from typing import Tuple, List


class TestNoughtsAndCrossesSearchAlgorithm:
    """
    Test class purely for testing the search algorithm of the NoughtsAndCrosses class
    (Chiefly its component methods)  # TODO write some tests for the winning_board_search method using components
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
        win, win_orientation = empty_game._winning_board_search()
        assert not win

    def test_no_win_empty_board(self, empty_game):
        empty_game.playing_grid = np.zeros(shape=(4, 3))
        win, win_orientation = empty_game._winning_board_search()
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
        win, win_orientation = empty_game._winning_board_search()
        assert win

    def test_horizontal_win_middle(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        win, win_orientation = empty_game._winning_board_search()
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
        win, win_orientation = empty_game._winning_board_search()
        assert win

    def test_vertical_win_top_right(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        win, win_orientation = empty_game._winning_board_search()
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
        win, win_orientation = empty_game._winning_board_search()
        assert win

    def test_south_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        win, win_orientation = empty_game._winning_board_search()
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
        win, win_orientation = empty_game._winning_board_search()
        assert win

    def test_north_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        win, win_orientation = empty_game._winning_board_search()
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


class TestNoughtsAndCrossesSearchLocationAlgorithm:
    """
    Test class purely for testing the search location algorithm of the NoughtsAndCrosses class
    This is the method that, once we know there is a win, locates exactly where it is
    """
    ##########
    # Tests for the search location algorithm
    ##########
    @pytest.fixture(scope="class")
    def empty_game_parameters(self):
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=5,
            game_cols_n=4,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def empty_game(self, empty_game_parameters):
        return NoughtsAndCrosses(setup_parameters=empty_game_parameters)

    def test_horizontal_win_top_right_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 1, 1, 1],
            [0, -1, 0, -1],
            [0, -1, 0, 1],
            [0, 0, 0, 1],
            [1, -1, 1, -1]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=0, col_index=2, win_orientation=WinOrientation.HORIZONTAL)
        expected_win_location = [(0, 1), (0, 2), (0, 3)]
        assert set(win_location) == set(expected_win_location)

    def test_horizontal_win_middle_left_location(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, -1],
            [-1, -1, -1, 1],
            [0, 0, 0, -1],
            [1, -1, 1, -1]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=2, col_index=1, win_orientation=WinOrientation.HORIZONTAL)
        expected_win_location = [(2, 0), (2, 1), (2, 2)]
        assert set(win_location) == set(expected_win_location)

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
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=2, col_index=0, win_orientation=WinOrientation.VERTICAL)
        expected_win_location = [(1, 0), (2, 0), (3, 0)]
        assert set(win_location) == set(expected_win_location)

    def test_vertical_win_middle_top_right(self, empty_game):
        empty_game.playing_grid = np.array([
            [-1, 1, 1, -1],
            [-1, 0, 1, 1],
            [-1, -1, 1, -1],
            [1, -1, -1, 0],
            [0, 0, 0, 0]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=0, col_index=2, win_orientation=WinOrientation.VERTICAL)
        expected_win_location = [(0, 2), (1, 2), (2, 2)]
        assert set(win_location) == set(expected_win_location)

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
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=3, col_index=3, win_orientation=WinOrientation.SOUTH_EAST)
        expected_win_location = [(1, 1), (2, 2), (3, 3)]
        assert set(win_location) == set(expected_win_location)

    def test_south_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 1, 0],
            [-1, -1, 0, 0],
            [0, -1, -1, 0]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=3, col_index=1, win_orientation=WinOrientation.SOUTH_EAST)
        expected_win_location = [(2, 0), (3, 1), (4, 2)]
        assert set(win_location) == set(expected_win_location)

    ##########
    # Tests for north east diagonal win
    ##########
    def test_north_east_win_lower_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 0, 0],
            [0, 0, 1, -1],
            [1, 0, -1, 0],
            [0, -1, 0, -1],
            [0, 0, -1, 0]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=1, col_index=3, win_orientation=WinOrientation.NORTH_EAST)
        expected_win_location = [(1, 3), (2, 2), (3, 1)]
        assert set(win_location) == set(expected_win_location)

    def test_north_east_win_upper_triangle_diag(self, empty_game):
        empty_game.playing_grid = np.array([
            [0, 0, 1, 0],
            [0, 1, 0, -1],
            [1, 0, -1, -1],
            [-1, -1, 0, 0],
            [1, -1, 1, -1]
        ])
        win_location: List[Tuple[int, int]] = empty_game.win_location_search(
            row_index=1, col_index=1, win_orientation=WinOrientation.NORTH_EAST)
        expected_win_location = [(0, 2), (1, 1), (2, 0)]
        assert set(win_location) == set(expected_win_location)