# Standard library imports
from typing import List, Tuple, Set
from dataclasses import dataclass

# Third party imports
import numpy as np

# Local application imports
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking, StartingPlayer
from game.app.win_check_location_search import win_check_and_location_search
from utils import np_array_to_tuple


@dataclass(frozen=False)
class NoughtsAndCrossesEssentialParameters:
    """
    Dataclass storing all the non-default setup_parameters for the Noughts and Crosses game.
    These are the setup_parameters that re necessary to fully define a game.
    """
    game_rows_m: int = None
    game_cols_n: int = None
    win_length_k: int = None
    player_x: Player = None
    player_o: Player = None
    starting_player_value: StartingPlayer = None


class NoughtsAndCrosses:
    """Base class with methods to manage the game play of a noughts and crosses game."""

    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters):
        self.game_rows_m = setup_parameters.game_rows_m
        self.game_cols_n = setup_parameters.game_cols_n
        self.win_length_k = setup_parameters.win_length_k
        self.player_x = setup_parameters.player_x
        self.player_o = setup_parameters.player_o
        self.starting_player_value = setup_parameters.starting_player_value
        self.playing_grid: np.ndarray = self._get_playing_grid(
            game_rows_m=self.game_rows_m, game_cols_n=self.game_cols_n, win_length_k=self.win_length_k)
        self.search_directions: List[np.ndarray] = self._get_search_directions(playing_grid=self.playing_grid)
        self.previous_mark_index: None | np.ndarray = None

    ##########
    # Methods that are a part of the core game play flow
    ##########
    def set_starting_player(self, starting_player_value: StartingPlayer = None) -> None:
        """
        Method to determine which player should go first given the starting_player_value (or not).
        This method initially maps as, f: StartingPlayer -> BoardMarking, f: {-1, 0, 1} |-> {-1, 1}, but note with no
        return - the outcome is to set the self.starting_player_value instance attribute as one of BoardMarking.X.value
        or BoardMarking.O.value.

        Parameters: starting_player_value - an enum value indicating whether it's player X, O or random to start first

        Note that the method only has an effect if the starting player is to be chosen RANDOMLY (0 starting player)
        """
        if starting_player_value is None:  # Included so the starting player can be reset for a new game
            starting_player_value = self.starting_player_value

        if starting_player_value == StartingPlayer.RANDOM.value or self.starting_player_value is None:
            self.starting_player_value = np.random.choice([BoardMarking.X.value, BoardMarking.O.value])
        elif starting_player_value == StartingPlayer.PLAYER_X.value:
            self.starting_player_value = BoardMarking.X.value
        elif starting_player_value == StartingPlayer.PLAYER_O.value:
            self.starting_player_value = BoardMarking.O.value
        else:
            raise ValueError("Attempted to call choose_starting_player method but with a starting_player_value"
                             " that is not in the StartingPlayer Enum. "
                             f"self.starting_player_value: {self.starting_player_value}")

    def get_player_turn(self, playing_grid: np.ndarray = None) -> BoardMarking:
        """
        Method to determine who's turn it is to mark the playing_grid, using the sum of the playing_grid 1s/-1s.
        If the sum is zero then both player's have had an equal number of turns, and therefore it's the starting
        player's turn. Otherwise, the starting player has had an extra go, so it's the other player's turn.

        Returns:
        BoardMarking value (1 or -1) - the piece that will get placed following the next turn.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        board_status = playing_grid.sum().real
        if board_status != 0:  # The starting player has had one more turn than the other player
            return BoardMarking(- self.starting_player_value).value
        else:
            return BoardMarking(self.starting_player_value).value

    def mark_board(self, marking_index: np.ndarray, playing_grid: np.ndarray = None) -> None:
        """
        Method to make a new entry on the game playing_grid. Note that this implementation ensures there is no
        opportunity to mark the board out of turn, because the marking made is always that of the next player.

        Parameters: marking_index - the index, as a numpy array, of the playing_grid where the mark will be made

        Outcomes:
        If the cell is empty, a mark is made with value corresponding to the player due to go next,
        else if a non-empty marking_index is passed, a value error is raised.
        The previous marking is then stored as the self.previous_mark_index attribute
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
            self.previous_mark_index = marking_index

        marking_index_tuple = np_array_to_tuple(marking_index)
        if playing_grid[marking_index_tuple] == BoardMarking.EMPTY.value:
            marking = self.get_player_turn(playing_grid=playing_grid)
            playing_grid[marking_index_tuple] = marking
        else:
            raise ValueError(f"mark_board attempted to mark non-empty cell at {marking_index}.")

    def win_check_and_location_search(self, last_played_index: np.ndarray, get_win_location: bool,
                                      playing_grid: np.ndarray = None) -> Tuple[bool, List[Tuple[int]] | None]:
        """
        Method to determine whether or not there is a win and the LOCATION of the win.
        See docstring for win_check_and_location_search, which is the function called in this method.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        winning_streak_found, win_streak_location_indexes = win_check_and_location_search(
            playing_grid=playing_grid,
            last_played_index=last_played_index,
            get_win_location=get_win_location,
            win_length_k=self.win_length_k,
            search_directions=self.search_directions
        )
        return winning_streak_found, win_streak_location_indexes

    def get_winning_player(self, winning_game: bool, playing_grid: np.ndarray = None) -> None | Player:
        """
        Method to return the winning player, given that we know there is a winning game scenario.

        Parameters: winning_game - True/False if this is a winning game scenario. RAISES a ValueError if False if passed
        playing_grid - The playing grid we are extracting the winning player from.

        Returns:
        None, or the winning player
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        previous_mark_made_by = - self.get_player_turn(playing_grid=playing_grid)
        if winning_game and (previous_mark_made_by == BoardMarking.X.value):
            return self.player_x
        elif winning_game and (previous_mark_made_by == BoardMarking.O.value):
            return self.player_o
        else:
            raise ValueError("Attempted to get_winning_player from a non-winning board scenario")

    def check_for_draw(self, playing_grid: np.ndarray = None) -> bool:
        """
        Method that checks whether or not the playing_grid has reached a stalemate. This is somewhat naive
        in that it just checks for a full playing_grid - a draw may in fact have been guaranteed sooner than the
        playing_grid being full, however this implementation is probably the fastest due to its simplicity.

        Returns: bool - T/F depending on whether the board has reached a draw
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        draw = np.all(playing_grid != BoardMarking.EMPTY.value)
        return draw

    def reset_game_board(self) -> None:
        """
        Method to reset the game playing_grid - all entries in the playing_grid are replaced with the empty cell value.
        The previous_marking_index is also set to its initial state of None.
        """
        self.previous_mark_index = None
        self.playing_grid = self._get_playing_grid(game_rows_m=self.game_rows_m, game_cols_n=self.game_cols_n,
                                                   win_length_k=self.win_length_k)

    # Lower level methods
    @staticmethod
    def _get_playing_grid(game_rows_m: int, game_cols_n: int, win_length_k: int) -> np.ndarray:
        """
        Method to create the playing_grid underpinning the entire game.
        This is represented by a numpy array
        """
        if win_length_k > max(game_rows_m, game_cols_n):
            raise ValueError(f"Attempted to create a playing grid which cannot be won on.\n"
                             f"Rows: {game_rows_m}, Columns: {game_cols_n}, Win length: {win_length_k}")
        else:
            playing_grid = np.full(shape=(game_rows_m, game_cols_n), fill_value=BoardMarking.EMPTY.value)
            return playing_grid

    @staticmethod
    def _get_search_directions(playing_grid: np.ndarray, array_list: List[np.ndarray] = None,
                               current_dimension: int = None) -> List[np.ndarray]:
        """
        Method that recursively returns the directions the search algorithm should look for a win in around the last
        played index, on an n-dimensional board.
        Starting with the one-dimensional array np.array([1]), we extend this to [1, 0], [1, 1] and [1, -1], and also
        add in [0, 1]. We then repeat the same process for EACH of these vectors at the next dimension, again
        adding the [0, 0, ..., 0, 1] vector.

        Parameters:
        ----------
        playing_grid: The playing grid we want the search directions for (only the dimensions matter)
        array_list: The list of search arrays in the lower dimension we are passing to the recursion to get the search
        directions in the higher dimension.
        current_dimension: The dimension we have just produced the search directions for, once this reaches the
        dimension of the playing grid, we stop the recursion

        Note that whenever we create a new array, it is essential here to specify dtype=int, otherwise indexing fails
        in the win search when we try to use floats as indexes.
        """
        if current_dimension is None:
            current_dimension = 0
            return NoughtsAndCrosses._get_search_directions(
                playing_grid=playing_grid, array_list=[np.array([1], dtype=int)],
                current_dimension=current_dimension + 1)
        elif current_dimension == np.ndim(playing_grid):
            return array_list
        else:
            new_array_list = []
            for arr in array_list:
                same_array_in_higher_d = np.concatenate((arr, np.array([0], dtype=int)))
                new_array_list.append(same_array_in_higher_d)

                new_array_one = np.concatenate((arr, np.array([1], dtype=int)))
                new_array_list.append(new_array_one)

                new_array_minus_one = np.concatenate((arr, np.array([-1], dtype=int)))
                new_array_list.append(new_array_minus_one)

            # Also add on the nth dimensional unit vector
            unit_array_nth_dim = np.zeros(current_dimension + 1, dtype=int)
            unit_array_nth_dim[current_dimension] = 1
            new_array_list.append(unit_array_nth_dim)
            return NoughtsAndCrosses._get_search_directions(
                playing_grid=playing_grid, array_list=new_array_list, current_dimension=current_dimension + 1)

    ##########
    # Whole board search method and ancillary methods
    ##########
    def whole_board_search(self) -> bool:
        """
        Method to check whether or not the playing_grid has reached a winning state.
        This is a whole board search, i.e. is naive to where the last move was played, and thus is only used
        when this information is not available.

        Returns:
        bool: True if a player has won, else false

        Notes: This is ~ O(n^2) slower than the win_check_and_location_search above. The speed however is highly
        dependent on the state of the board - the emptier the board, the quicker this is.
        """
        array_list = self.get_non_empty_array_list(playing_grid=self.playing_grid, win_length_k=self.win_length_k)
        for array in array_list:
            convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
            # "valid" kwarg means only where the np.ones array fully overlaps with the test array gets calculated
            real_convoluted_array = np.real(convoluted_array)
            max_consecutive = max(abs(real_convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # A win has been found
        return False  # No wins were found after looping through all the arrays

    @staticmethod
    def get_non_empty_array_list(playing_grid: np.ndarray, win_length_k: int) -> list[np.ndarray]:
        """
        Method to extract the rows, columns and diagonals that are non-empty from the playing grid.
        Note that this is only a two-dimensional method - would need to be extended for higher dimensional game.

        Parameters:
        __________
        playing_grid - included so that this method can check copies of the playing grid too
        win_length_K - the length of a win - used to clip diagonals that are not long enough to contain a win.

        Returns:
        __________
        A list of the arrays on the playing grid, of length at least self.win_length, to avoid arrays that are too short
        being searched unnecessarily.

        Notes: Tested the speed of using a filter and partial function to remove diagonals that are too short to
        contain a win, but this was slower than using a list comprehension.
        """
        # Get the indexes of the non-empty cells
        non_empty_cells: np.ndarray = np.argwhere(playing_grid != BoardMarking.EMPTY.value)

        # Non empty rows
        non_empty_row_indexes: Set[int] = {index[0] for index in non_empty_cells}
        row_array_list = [playing_grid[row_index] for row_index in non_empty_row_indexes]

        # Non empty columns
        non_empty_col_indexes: Set[int] = {index[1] for index in non_empty_cells}
        col_array_list = [playing_grid[:, col_index] for col_index in non_empty_col_indexes]

        # Non empty south east diagonal arrays long enough to contain a win
        non_empty_south_east_offsets: Set[int] = {(index[1] - index[0]) for index in non_empty_cells}
        full_south_east_list = [np.diagonal(playing_grid, offset) for offset in non_empty_south_east_offsets]
        # Could directly include the if statement here, but then would need to re-call the np.diagonal
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
