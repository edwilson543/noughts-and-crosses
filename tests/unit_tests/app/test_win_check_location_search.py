"""
Module for testing the the win check and location search algorithms.
"""

# Standard library imports
import pytest

# Third party imports
import numpy as np

# Local application imports
from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.app.win_check_location_search_n_dim import win_check_and_location_search
from game.constants.game_constants import StartingPlayer, BoardMarking


@pytest.fixture(scope="function")
def five_four_game_parameters():
    """
    Note that the starting_player_value is normally overridden during tests, but is included here for completeness.
    """
    return NoughtsAndCrossesEssentialParameters(
        game_rows_m=5,
        game_cols_n=4,
        win_length_k=3,
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def five_four_game(five_four_game_parameters):
    return NoughtsAndCrosses(setup_parameters=five_four_game_parameters)


@pytest.fixture(scope="module")
def search_directions():
    """Returns the (2D) search directions parameter to be used in the win check function"""
    return [np.array([1, 0]), np.array([0, 1]), np.array([1, -1]), np.array([1, 1])]


@pytest.fixture(scope="module")
def win_length_k():
    """Returns the wind length to be used in the win check function"""
    return 3


class TestNoughtsAndCrossesWinCheckAndSearchLocationFiveFour:
    """
    Test class for testing the win search location algorithm of the NoughtsAndCrosses class.
    All tests in this class test both the win bool value and win locations return.
    """
    def test_horizontal_win_top_right_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 1, 1, 1],
            [0, -1, 0, -1],
            [0, -1, 0, 1],
            [0, 0, 0, 1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([0, 3])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(0, 1), (0, 2), (0, 3)}
        assert win and (set(win_locations) == expected_win_location)

    def test_horizontal_win_middle_left_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, -1],
            [-1, -1, -1, 1],
            [0, 0, 0, -1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([2, 1])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(2, 0), (2, 1), (2, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_middle_left_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1, -1],
            [-1, -1, 1, 1],
            [-1, 1, -1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([2, 0])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(1, 0), (2, 0), (3, 0)}
        assert win and (set(win_locations) == expected_win_location)

    def test_vertical_win_middle_top_right(self, search_directions, win_length_k):
        playing_grid = np.array([
            [-1, 1, 1, -1],
            [-1, 0, 1, 1],
            [-1, -1, 1, -1],
            [1, -1, -1, 0],
            [0, 0, 0, 0]
        ])
        last_played_index = np.array([0, 2])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(0, 2), (1, 2), (2, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 0, 0],
            [-1, 1, 0, 0],
            [0, -1, 1, 0],
            [-1, 0, 0, 1],
            [1, -1, 0, 0]
        ])
        last_played_index = np.array([3, 3])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(1, 1), (2, 2), (3, 3)}
        assert win and (set(win_locations) == expected_win_location)

    def test_south_east_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 1, 0],
            [-1, -1, 0, 0],
            [0, -1, -1, 0]
        ])
        last_played_index = np.array([3, 1])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)

        expected_win_location = {(2, 0), (3, 1), (4, 2)}
        assert win and (set(win_locations) == expected_win_location)

    ##########
    # Tests for north east diagonal win
    ##########
    def test_south_west_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 0, 0],
            [0, 0, 1, -1],
            [1, 0, -1, 0],
            [0, -1, 0, -1],
            [0, 0, -1, 0]
        ])
        last_played_index = np.array([1, 3])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(1, 3), (2, 2), (3, 1)}
        assert win and (set(win_locations) == expected_win_location)

    def test_south_west_win_upper_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 1, 0],
            [0, 1, 0, -1],
            [1, 0, -1, -1],
            [-1, -1, 0, 0],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([1, 1])
        win, win_locations = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=True,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = {(0, 2), (1, 1), (2, 0)}
        assert win and (set(win_locations) == expected_win_location)


class TestNoughtsAndCrossesWinCheckOnlyFiveFour:
    """
    Test class purely for testing the win search location algorithm of the NoughtsAndCrosses class.
    All tests in this class test both the win bool value and win locations return.
    """
    def test_horizontal_win_top_right_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 1, 1, 1],
            [0, -1, 0, -1],
            [0, -1, 0, 1],
            [0, 0, 0, 1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([0, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_horizontal_win_middle_left_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, -1],
            [-1, -1, -1, 1],
            [0, 0, 0, -1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([2, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_middle_left_location(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1, -1],
            [-1, -1, 1, 1],
            [-1, 1, -1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([2, 0])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_vertical_win_middle_top_right(self, search_directions, win_length_k):
        playing_grid = np.array([
            [-1, 1, 1, -1],
            [-1, 0, 1, 1],
            [-1, -1, 1, -1],
            [1, -1, -1, 0],
            [0, 0, 0, 0]
        ])
        last_played_index = np.array([0, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 0, 0],
            [-1, 1, 0, 0],
            [0, -1, 1, 0],
            [-1, 0, 0, 1],
            [1, -1, 0, 0]
        ])
        last_played_index = np.array([3, 3])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_south_east_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 1, 0],
            [-1, -1, 0, 0],
            [0, -1, -1, 0]
        ])
        last_played_index = np.array([3, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Tests for north east diagonal win
    ##########
    def test_south_west_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 0, 0],
            [0, 0, 1, -1],
            [1, 0, -1, 0],
            [0, -1, 0, -1],
            [0, 0, -1, 0]
        ])
        last_played_index = np.array([2, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_south_west_win_upper_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 0, 1, 0],
            [0, 1, 0, -1],
            [1, 0, -1, -1],
            [-1, -1, 0, 0],
            [1, -1, 1, -1]
        ])
        last_played_index = np.array([1, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        expected_win_location = [(0, 2), (1, 1), (2, 0)]
        assert win


class TestNoughtsAndCrossesWinCheckOnlyFourThree:
    """
    Test class purely for testing the win check algorithm, for a four three game
    """
    ##########
    # Checks playing_grid is not a winner
    ##########
    def test_no_win_full_board(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1]
        ])
        last_played_index = np.array([0, 0])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert not win

    def test_no_win_empty_board(self, search_directions, win_length_k):
        playing_grid = np.zeros(shape=(4, 3))
        playing_grid[1, 1] = BoardMarking.X.value
        last_played_index = np.array([0, 0])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert not win

    ##########
    # Test for horizontal wins
    ##########
    def test_horizontal_win_top(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, 1, 1],
            [-1, 0, -1],
            [0, -1, 0],
            [0, 0, 0]
        ])
        last_played_index = np.array([0, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_horizontal_win_middle(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        last_played_index = np.array([2, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_vertical_win_bottom_left(self, search_directions, win_length_k):
        playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]
        ])
        last_played_index = np.array([3, 0])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_vertical_win_top_right(self, search_directions, win_length_k):
        playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        last_played_index = np.array([1, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Tests for south east diagonal win
    ##########

    def test_south_east_win_leading_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [-1, 1, 0],
            [0, -1, 1],
            [-1, 0, -1],
            [1, -1, 0]
        ])
        last_played_index = np.array([1, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_south_east_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        last_played_index = np.array([3, 2])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    ##########
    # Tests for north east diagonal win
    ##########

    def test_north_east_win_leading_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 1, -1],
            [1, -1, 0],
            [-1, 0, -1],
            [0, -1, 0]
        ])
        last_played_index = np.array([2, 0])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win

    def test_north_east_win_lower_triangle_diag(self, search_directions, win_length_k):
        playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        last_played_index = np.array([2, 1])
        win, _ = win_check_and_location_search(
            playing_grid=playing_grid, last_played_index=last_played_index, get_win_location=False,
            search_directions=search_directions, win_length_k=win_length_k)
        assert win
