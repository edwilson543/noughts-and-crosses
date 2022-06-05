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
        game_rows_m=5,
        game_cols_n=4,
        win_length_k=3,
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def empty_game(empty_game_parameters):
    return NoughtsAndCrosses(setup_parameters=empty_game_parameters)


class TestNoughtsAndCrossesNotSearches:
    """
    Test class to test the methods on the noughts and crosses class that are not search methods
    """
    def test_check_for_draw_draw_situation(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1],
            [1, -1, 1, -1],
            [-1, 1, -1, 1],
            [1, -1, 1, -1],
            [1, -1, 1, -1]
        ])
        draw = empty_game.check_for_draw()
        assert draw

# TODO test for the rest of the methods