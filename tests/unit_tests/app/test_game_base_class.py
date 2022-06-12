"""Module to test everything in the game base class, except for search methods."""

# Standard library imports
import pytest
from typing import List

# Third party imports
import numpy as np

# Local application imports
from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking


@pytest.fixture(scope="function")
def three_three_game_parameters():
    """
    Note that the starting_player_value is normally overridden during tests.
    """
    return NoughtsAndCrossesEssentialParameters(
        game_rows_m=3,
        game_cols_n=3,
        win_length_k=3,
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def three_three_game(three_three_game_parameters):
    return NoughtsAndCrosses(setup_parameters=three_three_game_parameters)


class TestNoughtsAndCrossesNotSearches:
    """
    Test class to test the methods on the noughts and crosses class that are not search methods
    """

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
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        three_three_game.mark_board(marking_index=np.array([2, 2]))
        assert three_three_game.playing_grid[2, 2] == BoardMarking.O.value  # O because X has had one more go

    def test_mark_board_non_empty_cell_raises_error(self, three_three_game):
        """
        Test that we can successfully mark an empty cell.
        Note that this method also calls get_player_turn
        """
        three_three_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        with pytest.raises(ValueError):
            three_three_game.mark_board(marking_index=np.array([0, 0]))

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

    def test_get_search_directions_two_dimensions(self, three_three_game):
        """Method to check that we can get the correct search direction in two dimensions."""
        expected_directions: List = [np.array([1, 0]), np.array([0, 1]), np.array([1, -1]), np.array([1, 1])]
        actual_directions: List = three_three_game._get_search_directions()

        # We want to test these lists are the same but note numpy arrays don't readily support __eq__
        for expected_array in expected_directions:  # Do the check below for each of the arrays
            expected_array_found = 0
            for actual_array in actual_directions:
                expected_array_found += np.all(actual_array == expected_array)
            assert expected_array_found  # This will be equal to 1 (True) if the array has been found

    def test_get_search_directions_three_dimensions(self, three_three_game):
        """
        Method to check that we can get the correct search direction in two dimensions.
        Note that this is an n-dimensional method, defined within the NoughtAndCrosses base class - because this base
        class currently uses a static 2D board, and it is not a static method, we need to test the 3D+ case using the
        unideal fix of calling the method on the (2D) three_three_game and passing in a 3D playing grid.

        Note also that the n-dimensional functionality here is mainly for a bit of fun.
        """
        expected_directions: List = [np.array([1, 0, 0]), np.array([1, 0, 1]), np.array([1, 0, -1]),
                                     np.array([1, 1, 0]), np.array([1, 1, 1]), np.array([1, 1, -1]),
                                     np.array([1, -1, 0]), np.array([1, -1, 1]), np.array([1, -1, -1]),
                                     np.array([0, 1, 0]), np.array([0, 1, 1]), np.array([0, 1, -1]),
                                     np.array([0, 0, 1])]

        three_dim_game_grid = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])  # we just need any old 3D array
        actual_directions: List = three_three_game._get_search_directions(playing_grid=three_dim_game_grid)

        # Using the methodology from the unit test above:
        for expected_array in expected_directions:
            expected_array_found = 0
            for actual_array in actual_directions:
                expected_array_found += np.all(actual_array == expected_array)
            assert expected_array_found


##########
# This is a test class for the whole board search (which is naive to where the last move was played)
##########
class TestNoughtsAndCrossesWholeBoardSearchAlgorithm:
    """
    Test class for the (old) whole board search algorithm of the NoughtsAndCrosses class (_winning_board_search)
    (Chiefly its component methods).
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
        win = four_three_game._whole_board_search()
        assert not win

    def test_no_win_empty_board(self, four_three_game):
        four_three_game.playing_grid = np.zeros(shape=(4, 3))
        win = four_three_game._whole_board_search()
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
        win = four_three_game._whole_board_search()
        assert win

    def test_horizontal_win_middle(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [-1, -1, -1],
            [0, 0, 0]
        ])
        win = four_three_game._whole_board_search()
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
        win = four_three_game._whole_board_search()
        assert win

    def test_vertical_win_top_right(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [-1, 1, 1],
            [-1, 1, 1],
            [-1, -1, 1],
            [1, -1, -1]
        ])
        win = four_three_game._whole_board_search()
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
        win = four_three_game._whole_board_search()
        assert win

    def test_south_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 1],
            [-1, 0, 1],
            [-1, -1, 0],
            [0, -1, -1]
        ])
        win = four_three_game._whole_board_search()
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
        win = four_three_game._whole_board_search()
        assert win

    def test_north_east_win_lower_triangle_diag(self, four_three_game):
        four_three_game.playing_grid = np.array([
            [0, 1, 0],
            [1, 0, -1],
            [0, -1, -1],
            [-1, -1, 0]
        ])
        win = four_three_game._whole_board_search()
        assert win

    ##########
    # Tests to see output of decomposing diagonals
    ##########
    def test_south_east_diagonal_list(self, four_three_game):
        """Tests whether the get_south_east_diagonal_list method is working"""
        four_three_game.game_rows_m = 5
        four_three_game.game_cols_n = 6
        four_three_game.playing_grid = np.arange(30).reshape((5, 6))
        # Using a set to avoid list order failing the test (which is irrelevant):
        expected_diagonal_arrays = [
            np.array([3, 10, 17]),
            np.array([2, 9, 16, 23]),
            np.array([1, 8, 15, 22, 29]),
            np.array([0, 7, 14, 21, 28]),
            np.array([6, 13, 20, 27]),
            np.array([12, 19, 26])
        ]
        actual_diagonal_arrays: list = four_three_game._get_south_east_diagonal_arrays(
            playing_grid=four_three_game.playing_grid)
        for act_array in actual_diagonal_arrays:
            validity = False
            for exp_array in expected_diagonal_arrays:
                validity += np.all(act_array == exp_array)
            assert validity

    def test_north_west_diagonal_list(self, four_three_game):
        """Tests whether the get_south_east_diagonal_list method is working"""
        four_three_game.game_rows_m = 5
        four_three_game.game_cols_n = 6
        four_three_game.playing_grid = np.arange(30).reshape((5, 6))
        # Using a set to avoid list order failing the test (which is irrelevant):
        expected_diagonal_arrays = [
            np.array([12, 7, 2]),
            np.array([18, 13, 8, 3]),
            np.array([24, 19, 14, 9, 4]),
            np.array([25, 20, 15, 10, 5]),
            np.array([26, 21, 16, 11]),
            np.array([27, 22, 17])
        ]
        actual_diagonal_arrays: list = four_three_game._get_north_east_diagonal_arrays()
        for act_array in actual_diagonal_arrays:
            validity = False
            for exp_array in expected_diagonal_arrays:
                validity += np.all(act_array == exp_array)
            assert validity
