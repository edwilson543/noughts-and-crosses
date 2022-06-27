"""
Module to test everything in the game base class, except for search methods.

Note that when testing methods that interact with the playing_grid, 0 is commonly used for brevity to represent an
empty cell, however the proper value is 1j (BoardMarking.EMPTY.value), which is used when a method directly compares
a cell value with the BoardMarking.EMPTY.value. For e.g. convolutions of a potential winning, 0 has no effect.
"""

# Standard library imports
import pytest
from typing import List

# Third party imports
import numpy as np

# Local application imports
from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking


class TestNoughtsAndCrossesGetPlayingGrid:
    """
    Test class for the short method for creating the initial game playing grid
    Tested separately as it's a static method, as is called at the initialisation of a new game, so does not use a
    fixture for a game instance, as for the other methods.
    """

    def test_get_playing_grid_valid_dimensions(self):
        rows = 3
        columns = 3
        win_length = 3
        actual_playing_grid = NoughtsAndCrosses._get_playing_grid(game_rows_m=rows, game_cols_n=columns,
                                                                  win_length_k=win_length)
        expected_playing_grid = np.full(shape=(rows, columns), fill_value=BoardMarking.EMPTY.value)
        assert np.all(actual_playing_grid == expected_playing_grid)

    def test_get_playing_grid_rows_and_cols_too_short(self):
        rows = 3
        columns = 3
        win_length = 4
        with pytest.raises(ValueError):
            actual_playing_grid = NoughtsAndCrosses._get_playing_grid(game_rows_m=rows, game_cols_n=columns,
                                                                      win_length_k=win_length)

    def test_get_playing_grid_rows_long_enough_but_cols_not(self):
        """We can still play on a grid where one of rows / columns is long enough to contain a winning streak"""
        rows = 4
        columns = 3
        win_length = 4
        actual_playing_grid = NoughtsAndCrosses._get_playing_grid(game_rows_m=rows, game_cols_n=columns,
                                                                  win_length_k=win_length)
        expected_playing_grid = np.full(shape=(rows, columns), fill_value=BoardMarking.EMPTY.value)
        assert np.all(actual_playing_grid == expected_playing_grid)


class TestNoughtsAndCrossesMethodsNotSearches:
    """Test class to test the methods on the noughts and crosses class that are not search methods"""

    @pytest.fixture(scope="function")
    def three_three_game_parameters(self):
        """
        Note that the starting_player_value is normally overridden during tests, hence scope=function here.
        """
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=3,
            game_cols_n=3,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def three_three_game(self, three_three_game_parameters):
        return NoughtsAndCrosses(setup_parameters=three_three_game_parameters)

    # set_starting_player tests
    def test_set_starting_player_randomly(self, three_three_game):
        """Test that the set_starting_player method picks a valid BoardMarking member as the starting player"""
        three_three_game.starting_player_value = StartingPlayer.RANDOM.value
        three_three_game.set_starting_player()
        permitted_starting_player_values = [BoardMarking.X.value, BoardMarking.O.value]
        assert three_three_game.starting_player_value in permitted_starting_player_values

    def test_set_starting_player_as_x(self, three_three_game):
        three_three_game.starting_player_value = StartingPlayer.PLAYER_X.value
        three_three_game.set_starting_player()
        assert three_three_game.starting_player_value == BoardMarking.X.value

    def test_set_starting_player_as_o(self, three_three_game):
        three_three_game.starting_player_value = StartingPlayer.PLAYER_O.value
        three_three_game.set_starting_player()
        assert three_three_game.starting_player_value == BoardMarking.O.value

    # get_player_turn tests
    def test_get_player_turn_not_starting_player(self, three_three_game):
        """
        Test that when one player has had more goes than the other player, the other player goes next,
        according to the get_player_turn_method.
        """
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        player_turn = three_three_game.get_player_turn()
        assert player_turn == BoardMarking.O.value

    def test_get_player_turn_back_to_starting_player(self, three_three_game):
        """
        Test that when both player's have had an equal number of goes, the get_player_turn method identifies
        the starting player as the player to who's turn it is next.
        """
        three_three_game.starting_player_value = StartingPlayer.PLAYER_O.value
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [BoardMarking.O.value, 0, 0],
            [0, 0, 0]
        ])
        player_turn = three_three_game.get_player_turn()
        assert player_turn == BoardMarking.O.value

    # mark_board tests
    def test_mark_board_empty_cell(self, three_three_game):
        """
        Test that we can successfully mark an empty cell.
        Note that this method also calls get_player_turn
        """
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value],
            [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value],
            [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value]
        ])
        three_three_game.mark_board(marking_index=np.array([2, 2]))
        assert three_three_game.playing_grid[2, 2] == BoardMarking.O.value  # O because X has had one more go

    def test_mark_board_non_empty_cell_raises_error(self, three_three_game):
        """
        Test that we can successfully mark an empty cell.
        Note that this method also calls get_player_turn
        """
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value],
            [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value],
            [BoardMarking.EMPTY.value, BoardMarking.EMPTY.value, BoardMarking.EMPTY.value]
        ])
        with pytest.raises(ValueError):
            three_three_game.mark_board(marking_index=np.array([0, 0]))

    # win check test
    def test_horizontal_win_bottom(self, three_three_game):
        """Check that the win_check_and_location_search is properly linked into the method."""
        three_three_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1]
        ])
        win, _ = three_three_game.win_check_and_location_search(
            last_played_index=np.array([2, 2]), get_win_location=False)
        assert win

    # get_winning_player tests
    def test_get_winning_player_player_x_has_win(self, three_three_game):
        """Test that the winning player is correctly extracted by the get winning player method"""
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, BoardMarking.X.value, BoardMarking.X.value],
            [BoardMarking.O.value, BoardMarking.O.value, 0],
            [0, 0, 0]
        ])
        winning_player = three_three_game.get_winning_player(winning_game=True)
        assert winning_player == three_three_game.player_x

    def test_get_winning_player_no_winner(self, three_three_game):
        """Test that a ValueError is raised when False is passed to the get winning player method"""
        with pytest.raises(ValueError):
            three_three_game.get_winning_player(winning_game=False)

    # check_for_draw tests
    def test_check_for_draw_draw_situation(self, three_three_game):
        """Test that a full playing board returns a True for check_for_draw"""
        three_three_game.playing_grid = np.array([
            [1, -1, 1],
            [1, -1, 1],
            [-1, 1, -1]
        ])
        draw = three_three_game.check_for_draw()
        assert draw

    def test_check_for_draw_not_draw_situation(self, three_three_game):
        """Test that a playing board that is not full returns a False for check_for_draw"""
        three_three_game.playing_grid = np.array([
            [BoardMarking.EMPTY.value, 1, 1],
            [-1, -1, 1],
            [-1, 1, -1]
        ])
        draw = three_three_game.check_for_draw()
        assert not draw

    # reset_game_board test
    def test_reset_game_board(self, three_three_game):
        """Test that the reset_game_board method correctly clears the game board"""
        three_three_game.playing_grid = np.array([
            [BoardMarking.EMPTY.value, 1, 1],
            [-1, -1, 1],
            [-1, 1, -1]
        ])
        three_three_game.previous_mark_index = np.array([0, 2])
        three_three_game.reset_game_board()

        assert np.all(three_three_game.playing_grid == BoardMarking.EMPTY.value)
        assert three_three_game.previous_mark_index is None

    # _get_search_directions_tests
    def test_get_search_directions_two_dimensions(self, three_three_game):
        """Method to check that we can get the correct search direction in two dimensions."""
        expected_directions: List = [np.array([1, 0]), np.array([0, 1]), np.array([1, -1]), np.array([1, 1])]
        actual_directions: List = three_three_game._get_search_directions(playing_grid=three_three_game.playing_grid)

        # We want to test these lists are the same but note numpy arrays don't readily support __eq__
        for expected_array in expected_directions:  # Do the check below for each of the arrays
            expected_array_found = 0
            for actual_array in actual_directions:
                expected_array_found += np.all(actual_array == expected_array)
            assert expected_array_found  # This will be equal to 1 (True) if the array has been found

    def test_get_search_directions_three_dimensions(self):
        """
        Method to check that we can get the correct search direction in three dimensions.
        Note that the n-dimensional functionality here is mainly for a bit of fun.
        """
        expected_directions: List = [np.array([1, 0, 0]), np.array([1, 0, 1]), np.array([1, 0, -1]),
                                     np.array([1, 1, 0]), np.array([1, 1, 1]), np.array([1, 1, -1]),
                                     np.array([1, -1, 0]), np.array([1, -1, 1]), np.array([1, -1, -1]),
                                     np.array([0, 1, 0]), np.array([0, 1, 1]), np.array([0, 1, -1]),
                                     np.array([0, 0, 1])]

        three_dim_game_grid = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])  # we just need any old 3D array
        actual_directions: List = NoughtsAndCrosses._get_search_directions(playing_grid=three_dim_game_grid)

        # Using the methodology from the unit test above:
        for expected_array in expected_directions:
            expected_array_found = 0
            for actual_array in actual_directions:
                expected_array_found += np.all(actual_array == expected_array)
            assert expected_array_found


class TestNoughtsAndCrossesWholeBoardSearchAlgorithmFourThreeGame:
    """
    Test class for the whole board search algorithm of the NoughtsAndCrosses class, and ancillary methods,
    on the four three game.
    """

    @pytest.fixture(scope="class")
    def four_three_game_parameters(self):
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=4,
            game_cols_n=3,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def four_three_game(self, four_three_game_parameters):
        return NoughtsAndCrosses(setup_parameters=four_three_game_parameters)

    ##########
    # Checks playing_grid does not have a winner
    ##########
    def test_no_win_full_board(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, -1, 1],
            [-1, -1, 1],
            [1, 1, -1],
            [-1, 1, -1]
        ])
        win = four_three_game.whole_board_search()
        assert not win

    def test_no_win_empty_board(self, four_three_game):
        four_three_game.playing_grid = np.zeros(shape=(4, 3))
        win = four_three_game.whole_board_search()
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
        win = four_three_game.whole_board_search()
        assert win

    def test_horizontal_win_middle(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        win = four_three_game.whole_board_search()
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
        win = four_three_game.whole_board_search()
        assert win

    def test_vertical_win_top_right(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        win = four_three_game.whole_board_search()
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
        win = four_three_game.whole_board_search()
        assert win

    def test_south_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        win = four_three_game.whole_board_search()
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
        win = four_three_game.whole_board_search()
        assert win

    def test_north_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        win = four_three_game.whole_board_search()
        assert win


class TestNoughtsAndCrossesGetNoneEmptyArrayListFiveSixGame:
    """
    Test class for the get_non_empty_array_list of the NoughtsAndCrosses class on a five-six game.
    """

    @pytest.fixture(scope="class")
    def five_six_game_parameters(self):
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=5,
            game_cols_n=6,
            win_length_k=3,
            starting_player_value=StartingPlayer.PLAYER_X.value)

    @pytest.fixture(scope="function")
    def five_six_game(self, five_six_game_parameters):
        return NoughtsAndCrosses(setup_parameters=five_six_game_parameters)

    def test_get_non_empty_array_list(self, five_six_game):
        """Tests whether the get_south_east_diagonal_list method is working"""
        five_six_game.playing_grid = np.arange(30).reshape((5, 6))
        # Using a set to avoid list order failing the test (which is irrelevant):
        expected_row_arrays = [
            np.array([0, 1, 2, 3, 4, 5]),
            np.array([6, 7, 8, 9, 10, 11]),
            np.array([12, 13, 14, 15, 16, 17]),
            np.array([18, 19, 20, 21, 22, 23]),
            np.array([24, 25, 26, 27, 28, 29]),
        ]
        expected_column_arrays = [
            np.array([0, 6, 12, 18, 24]),
            np.array([1, 7, 13, 19, 25]),
            np.array([2, 8, 14, 20, 26]),
            np.array([3, 9, 15, 21, 27]),
            np.array([4, 10, 16, 22, 28]),
            np.array([5, 11, 17, 23, 29])
        ]
        expected_south_east_diagonal_arrays = [
            np.array([3, 10, 17]),
            np.array([2, 9, 16, 23]),
            np.array([1, 8, 15, 22, 29]),
            np.array([0, 7, 14, 21, 28]),
            np.array([6, 13, 20, 27]),
            np.array([12, 19, 26])
        ]
        expected_south_west_diagonal_arrays = [
            np.array([2, 7, 12]),
            np.array([3, 8, 13, 18]),
            np.array([4, 9, 14, 19, 24]),
            np.array([5, 10, 15, 20, 25]),
            np.array([11, 16, 21, 26]),
            np.array([17, 22, 27])
        ]
        all_expected_arrays = expected_row_arrays + expected_column_arrays + expected_south_east_diagonal_arrays + \
                              expected_south_west_diagonal_arrays
        all_actual_arrays: list = five_six_game.get_non_empty_array_list(
            playing_grid=five_six_game.playing_grid, win_length_k=five_six_game.win_length_k)
        for exp_array in all_expected_arrays:
            validity = False
            for act_array in all_actual_arrays:
                validity += np.all(exp_array == act_array)
            assert validity
