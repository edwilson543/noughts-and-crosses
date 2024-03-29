"""
Module defining the main win checker and win location finder for the playing grid.
Note that this is an n-dimensional method due to the generality afforded by the search_directions argument.
"""

# Standard library imports
from typing import Tuple, List

# Third party imports
import numpy as np

# Local application imports
from game.app.win_check_cache_decorator import LRUCacheWinSearch


@LRUCacheWinSearch(maxsize=1000000, use_symmetry=False)
def win_check_and_location_search(playing_grid: np.ndarray, last_played_index: np.ndarray,
                                  get_win_location: bool, search_directions: List[np.ndarray],
                                  win_length_k: int) -> Tuple[bool, List[Tuple[int]] | None]:
    """
    Method to determine whether or not there is a win and the LOCATION of the win.
    get_win_location controls whether we are interested in the win_location or not. Note that having a separate
    method to find the win location would introduce huge redundancy as all variables used to check for a
    win are needed to find the win location, hence the slightly longer method.

    Parameters:
    ----------
    playing_grid - the board we are searching for a win

    last_played_index - where the last move on the board was made, to restrict the search area, represented by a
    numpy array

    get_win_location - if this is True then the method returns the win locations as well, if it's false then the
    only return is a bool for whether or not the board exhibits a win

    search_directions - the directions from the last played index that we are searching for a win in

    win_length - the length of winning streak we are searching for

    Returns:
    ----------
    bool - T/F depending on whether or not there is a win
    List[Tuple[int]] - A list of the indexes corresponding to the winning streak (only if get_win_location is
    set to True)

    Other information:
    ----------
    This function only searches the intersection of the self.win_length - 1 boundary around the last move with the
    board, making it much faster than searching the entire board for a win.
    Determining the location of the win adds extra processing, increasing the runtime of the search, therefore when
    the win location is NOT needed (e.g. in the minimax algorithm), the get_win_location should be set to False.
    """

    for search_direction in search_directions:
        unfiltered_indexes_to_search: list = [tuple(last_played_index + offset * search_direction)
                                              for offset in range(-win_length_k + 1, win_length_k)]
        valid_search_ranges = [range(0, playing_grid.shape[n]) for n in range(0, np.ndim(playing_grid))]
        valid_indexes_to_search: list = [search_index for search_index in unfiltered_indexes_to_search if
                                         all(search_index[n] in valid_search_ranges[n] for n in
                                             range(0, np.ndim(playing_grid)))]
        # This is an n-dimensional bound on the indexes generated by unfiltered_indexes_to_search
        array_to_search = np.array([playing_grid[search_index] for search_index in valid_indexes_to_search])
        real_array_to_search = np.real(array_to_search)
        streak_lengths = abs(np.convolve(real_array_to_search, np.ones(win_length_k, dtype=int), mode="valid"))
        winning_streak_found: bool = max(streak_lengths) == win_length_k

        if winning_streak_found and not get_win_location:
            return winning_streak_found, None
        elif winning_streak_found and get_win_location:
            win_streak_start_index = np.where(streak_lengths == win_length_k)
            win_streak_start_int: int = np.array(win_streak_start_index).item(0)
            # .item() avoids issue with dimensions - it extracts the scalar value, regardless of current_dimension
            win_streak_location_indexes: list = valid_indexes_to_search[
                                                win_streak_start_int: win_streak_start_int + win_length_k]
            return winning_streak_found, win_streak_location_indexes
    else:
        return False, None  # No win has been found, and thus no winning location
