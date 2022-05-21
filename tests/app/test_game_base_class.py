from game.app.game_base_class import NoughtsAndCrosses
import pytest
import numpy as np

@pytest.fixture(scope="module")
def test_rows():
    return 4

@pytest.fixture(scope="module")
def test_cols():
    return 6

@pytest.fixture(scope="module")
def test_win_length():
    return 3


class TestNoughtsAndCrossesSearchAlgorithm:
    """Test class purely for testing the search algorithm of the NoughtsAndCrosses class"""

    # noinspection PyTypeChecker
    @pytest.fixture(scope="function")
    def empty_game(self, test_rows, test_cols, test_win_length):
        return NoughtsAndCrosses(
            game_rows_m=test_rows,
            game_cols_n=test_rows,
            win_length_k=test_win_length,
            pos_player=None,
            neg_player=None,
            starting_player=None)


    def test_horizontal_win_top_left(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [-1, 1, -1, 1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid)
        assert win
