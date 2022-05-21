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
            game_cols_n=test_cols,
            win_length_k=test_win_length,
            pos_player=None,
            neg_player=None,
            starting_player=None)

    ##########
    # Checks for horizontal wins (or not)
    ##########
    def test_no_horizontal_win(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [-1, 1, -1, 1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid, row_count=empty_game.game_rows_m)
        assert not win

    def test_horizontal_win_top_left(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, 1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [-1, 1, -1, 1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid, row_count=empty_game.game_rows_m)
        assert win

    def test_horizontal_win_middle(self, empty_game):
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [-1, 1, -1, -1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid, row_count=empty_game.game_rows_m)
        assert win

    ##########
    # Test for vertical wins
    ##########
    def test_no_vertical_win(self, empty_game):
        empty_game.playing_grid = np.array
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, -1],
            [1, 1, -1, 1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid.transpose(),
                                                  row_count=empty_game.game_cols_n)
        assert not win

    def test_vertical_win_bottom_left(self, empty_game):
        empty_game.playing_grid = np.array
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid.transpose(),
                                                  row_count=empty_game.game_cols_n)
        assert win

    def test_vertical_win_top_right(self, empty_game):
        empty_game.playing_grid = np.array
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [1, -1, 1, -1, -1, 1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid.transpose(),
                                                  row_count=empty_game.game_cols_n)
        assert win

    def test_vertical_win_middle(self, empty_game):
        empty_game.playing_grid = np.array
        empty_game.playing_grid = np.array([
            [1, -1, 1, -1, 1, 1],
            [-1, -1, 1, -1, 1, 1],
            [1, 1, -1, 1, 1, -1],
            [-1, 1, -1, 1, -1, -1]
        ])
        win = empty_game.check_for_horizontal_win(playing_grid=empty_game.playing_grid.transpose(),
                                                  row_count=empty_game.game_cols_n)
        assert win

    ##########
    # Tests for diagonal win
    ##########
