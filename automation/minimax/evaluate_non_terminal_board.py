"""
Module to define how the board should be scored from the maximiser's perspective when
the board is not terminal.
With the introduction of iterative deepening and a time out, the vast majority of calls end in
an early evaluation (i.e. a non-terminal board), and so a scoring system is needed that indicates how favourable
a board is for later in the game.

This could ultimately use a transposition table derived from previous games.
"""

# Standard library imports
from typing import Tuple, List, Set

# Third party imports
import numpy as np

# Local application imports
from game.app.win_check_cache_decorators import LRUCacheWinSearch


# @LRUCacheWinSearch(hash_key_kwargs={"playing_grid", "get_win_location"}, maxsize=1000000, use_symmetry=True)
def non_terminal_board_score(playing_grid: np.ndarray,
                             last_played_index: np.ndarray,
                             search_directions: List[np.ndarray],
                             win_length_k: int) -> int:
    """
    Method to determine the score that should be assigned to a board, from the perspective of the maximising player who
    is here assumed to be the player who's turn it is.
    The idea is to identify any streaks of significant length and assign a score to these. For example, if we find
    a board

    Parameters:
    ----------
    playing_grid - the board we are searching for a win

    last_played_index - where the last move on the board was made, to restrict the search area, represented by a
    numpy array

    get_win_location - if this is True then the method returns the win locations as well, if it's false then the
    only return is a bool for whether or not the board exhibits a win

    search_directions - the directions from the last played index that we are searching for a win in

    win_length - the length of winning streak we are searching for

    """
    pass

    def evaluate_non_terminal_board(playing_grid: np.ndarray = None) -> bool:
        """
        """
        win_orientation = None
        if playing_grid is None:
            playing_grid = self.playing_grid

        row_win = self._search_array_list_for_win(
            array_list=self._get_row_arrays(playing_grid=playing_grid))
        col_win = self._search_array_list_for_win(
            array_list=self._get_col_arrays(playing_grid=playing_grid))
        south_east_win = self._search_array_list_for_win(
            array_list=self._get_south_east_diagonal_arrays(playing_grid=playing_grid))
        north_east_win = self._search_array_list_for_win(
            array_list=self._get_north_east_diagonal_arrays(playing_grid=playing_grid))

        return bool(row_win + col_win + south_east_win + north_east_win)

    #  Methods called in _winning_board_search
    def _score_individual_array(array: np.ndarray) -> int:
        """
        # TODO
        By convolving with a ones array of length win_length_k, this gives us an idea of whether an incomplete streak
        could be completed - (1, 1, 1) . (1, 1, 0) = 2, where as (1, 1, 1) . (1, 1, -1) = 1
        """
        # for array in array_list:
        #     convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
        #     # "valid" kwarg means only where the np.ones a fully overlaps with the row gets calculated
        #     max_consecutive = max(abs(convoluted_array))
        #     if max_consecutive == self.win_length_k:
        #         return True  # Diagonals contains a winning a
        # return False  # The algorithm has looped over all south-east diagonals and not found any winning boards

    def _get_non_empty_array_list(playing_grid: np.ndarray, win_length_k: int) -> list[np.ndarray]:
        """
        Method to extract the rows, columns and diagonals that are non-empty from the playing grid

        Parameters:
        __________
        playing_grid - so that this method can be re-used to check for north east diagonals too, and in the minimax ai

        Returns:
        __________
        A list of the south east diagonal arrays on the playing grid, of length at least self.win_length.
        i.e. south east diagonal arrays too short to contain a winning streak are intentionally excluded, to avoid
        being searched unnecessarily.
        """
        # Get the indexes of the non-empty cells
        non_empty_cells: np.ndarray = np.arghwere(playing_grid != 0)

        # Non empty rows
        non_empty_row_indexes: Set[int] = {index[0] for index in non_empty_cells}
        row_array_list = [playing_grid[row_index] for row_index in non_empty_row_indexes]

        # Non empty columns
        non_empty_col_indexes: Set[int] = {index[1] for index in non_empty_cells}
        col_array_list = [playing_grid[:, col_index] for col_index in non_empty_col_indexes]

        # Non empty south east diagonal arrays long enough to contain a win
        non_empty_south_east_offsets: Set[int] = {(index[1] - index[0]) for index in non_empty_cells}
        full_south_east_list = [np.diagonal(playing_grid, offset) for offset in non_empty_south_east_offsets]
        valid_south_east_diagonals = [diagonal_array for diagonal_array in full_south_east_list if
                                      len(diagonal_array) >= win_length_k]

        # Non empty south west diagonal arrays long enough to contain a win
        n_cols = playing_grid.shape[1]  # We flip the playing_grid left-to-right so also need to flip the col index lr
        non_empty_south_west_offsets: Set[int] = {((n_cols - index[1] - 1) - index[0]) for index in non_empty_cells}
        full_south_west_list = [np.fliplr(playing_grid).diagonal(offset=offset) for
                                offset in non_empty_south_west_offsets]
        valid_south_west_diagonals = [diagonal_array for diagonal_array in full_south_west_list if
                                      len(diagonal_array) >= win_length_k]

        return row_array_list + col_array_list + valid_south_east_diagonals + valid_south_west_diagonals
