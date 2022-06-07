"""Module to test everything in the game base class, except for search methods."""

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
        game_rows_m=3,
        game_cols_n=3,
        win_length_k=3,
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def empty_game(empty_game_parameters):
    return NoughtsAndCrosses(setup_parameters=empty_game_parameters)


class TestNoughtsAndCrossesNotSearches:
    """
    Test class to test the methods on the noughts and crosses class that are not search methods
    """
    # check_for_draw tests
    def test_check_for_draw_draw_situation(self, empty_game):
        """Test that a full playing board returns a True for check_for_draw"""
        empty_game.playing_grid = np.array([
            [1, -1, 1],
            [1, -1, 1],
            [-1, 1, -1]
        ])
        draw = empty_game.check_for_draw()
        assert draw

    # get_player_turn tests
    def test_get_player_turn_not_starting_player(self, empty_game):
        """
        Test that when one player has had more goes than the other player, the other player goes next,
        according to the get_player_turn_method.
        """
        empty_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        player_turn = empty_game.get_player_turn()
        assert player_turn == BoardMarking.O.value

    def test_get_player_turn_back_to_starting_player(self, empty_game):
        """
        Test that when both player's have had an equal number of goes, the get_player_turn method identifies
        the starting player as the player to who's turn it is next.
        """
        empty_game.starting_player_value = StartingPlayer.PLAYER_O.value
        empty_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [BoardMarking.O.value, 0, 0],
            [0, 0, 0]
        ])
        player_turn = empty_game.get_player_turn()
        assert player_turn == BoardMarking.O.value

    # mark_board tests
    def test_mark_board_empty_cell(self, empty_game):
        """
        Test that we can successfully mark an empty cell.
        Note that this method also calls get_player_turn
        """
        empty_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        empty_game.mark_board(marking_index=np.array([2, 2]))
        assert empty_game.playing_grid[2, 2] == BoardMarking.O.value  # O because X has had one more go

    def test_mark_board_non_empty_cell_raises_error(self, empty_game):
        """
        Test that we can successfully mark an empty cell.
        Note that this method also calls get_player_turn
        """
        empty_game.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        with pytest.raises(ValueError):
            empty_game.mark_board(marking_index=np.array([0, 0]))

    # get_winning_player tests
    # TODO
