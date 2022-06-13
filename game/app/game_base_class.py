# Standard library imports
from typing import List, Tuple
from dataclasses import dataclass

# Third party imports
import numpy as np

# Local application imports
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking, StartingPlayer, BoardString
from game.app.win_check_location_search import win_check_and_location_search


@dataclass(frozen=False)
class NoughtsAndCrossesEssentialParameters:
    """
    Dataclass storing all the non-default setup_parameters for the Noughts and Crosses game.
    These are the setup_parameters that re necessary to fully define a game.

    starting_player_value is stored as a BoardMarking value (either 1 or -1)
    """
    game_rows_m: int = None
    game_cols_n: int = None
    win_length_k: int = None
    player_x: Player = None
    player_o: Player = None
    starting_player_value: StartingPlayer = None


class NoughtsAndCrosses:
    """Base class to reflect the game play of a noughts and crosses game."""

    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters):
        self.game_rows_m = setup_parameters.game_rows_m
        self.game_cols_n = setup_parameters.game_cols_n
        self.win_length_k = setup_parameters.win_length_k
        self.player_x = setup_parameters.player_x
        self.player_o = setup_parameters.player_o
        self.starting_player_value = setup_parameters.starting_player_value
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n), dtype=int)
        self.search_directions = self._get_search_directions()

    ##########
    # Methods that are a part of the core game play flow
    ##########
    def set_starting_player(self, starting_player_value=None) -> None:
        """
        Method to determine which board marking should go first from a starting_player_value choice.
        This method is a function, f: StartingPlayer -> BoardMarking, f: {-1, 0, 1} |-> {-1, 1}, and thus only
        has an effect if the starting player is to be chosen RANDOMLY.
        """
        if starting_player_value is None:
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
        Method to determine who's turn it is to mark the playing_grid, using sum of the playing_grid 1s/-1s.
        If the sum is zero then both player's have had an equal number of turns, and therefore it's the starting
        player's turn. Otherwise, the starting player has had an extra go, so it's the other player's turn.

        Returns:
        BoardMarking value (1 or -1) - the piece that will get placed following the next turn.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        board_status = playing_grid.sum().sum()
        if board_status != 0:  # The starting player has had one more turn than the other player
            return BoardMarking(-self.starting_player_value).value
        else:
            return BoardMarking(self.starting_player_value).value

    def mark_board(self, marking_index: np.ndarray, playing_grid: np.ndarray = None) -> None:
        """
        Method to make a new entry on the game playing_grid. Note that there is no opportunity to mark out of
        turn, because the get_player_turn method is called within this method.
        Parameters:
        marking_index - the index, as a numpy a, of the playing_grid where the mark will be made
        playing_grid - the playing grid or copy that we are marking
        Returns:
        None
        Outcomes:
        If the cell is empty, a mark is made, else a value error is raised
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        if playing_grid[tuple(marking_index)] == 0:
            marking = self.get_player_turn(playing_grid=playing_grid)
            playing_grid[tuple(marking_index)] = marking
        else:
            raise ValueError(f"mark_board attempted to mark non-empty cell at {marking_index}.")

    def win_check_and_location_search(self, last_played_index: np.ndarray, get_win_location: bool,
                                      playing_grid: np.ndarray = None) -> Tuple[bool, List[Tuple[int]] | None]:
        """
        Method to determine whether or not there is a win and the LOCATION of the win.
        This method just calls the win_check_and_location function is it located in its own module. See the docstring
        of that function for more information.

        Parameters: ---------- last_played_index - where the last move on the board was made, to restrict the search
        area, represented by a numpy a

        get_win_location - if this is True then the method returns the win locations as well, if it's false then the
        only return is a bool for whether or not the board exhibits a win

        playing_grid - the board we are searching for a win

        Returns:
        ----------
        bool - T/F depending on whether or not there is a win
        List[Tuple[int]] - A list of the indexes corresponding to the winning streak (only if get_win_location is
        set to True, otherwise None)

        Other information:
        ----------
        This method only searches the intersection of the self.win_length - 1 boundary around the last move with the
        board, making it much faster than searching the entire board for a win.
        Determining the location of the win adds extra processing, increasing the runtime of the search, therefore when
        the win location is NOT needed (e.g. in the minimax algorithm), the get_win_location should be set to False.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        return_val = win_check_and_location_search(
            playing_grid=playing_grid,
            last_played_index=last_played_index,
            get_win_location=get_win_location,
            win_length_k=self.win_length_k,
            search_directions=self.search_directions
        )
        return return_val

    def get_winning_player(self, winning_game: bool, playing_grid: np.ndarray = None) -> None | Player:
        """
        Method to return the winning player, given that we know there is a winning game scenario

        Parameters: __________ winning_game: True/False if this is a winning game scenario. RAISES
        a ValueError if False if passed playing_grid: The playing grid we are extracting the winning player
        from

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
        Method that checks whether or not the playing_grid has reached a stalemate. This is currently naive
        in that it just checks for a full playing_grid - a draw may in fact have been guaranteed
        sooner than the playing_grid being full. #  TODO think about how to address this

        Parameters: playing_grid, to allow re-use for minimax
        Returns: bool - T/F depending on whether the board has reached a draw
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        draw = np.all(playing_grid != 0)
        return draw

    def reset_game_board(self) -> None:
        """Method to reset the game playing_grid - replaces all entries in the playing_grid with a zero"""
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n))

    # Lower level methods
    def _get_search_directions(self, playing_grid: np.ndarray = None, array_list: List[np.ndarray] = None,
                               dimension: int = None) -> List[np.ndarray]:
        """
        Method that recursively returns the directions the search algorithm should look for a win in around the last
        played index.
        Starting with the one-dimensional array np.array([1]), we extend this to [1, 0], [1, 1] and [1, -1], also
        adding in [0, 1]. We then repeat the same process for each of these vectors at the next dimension, again
        adding the [0, 0, ..., 0, 1] vector.

        Parameters:
        ----------
        playing_grid: The playing grid we are searching for a win
        array_list: The list of search arrays in the lower dimension we are passing to the recursion to get the search
        direction in the higher dimension.
        dimension: The dimension we have just produced the search directions for, once this reaches the dimension of
        the playing grid, we stop the recursion

        Note that whenever we create a new array, it is essential here to specify dtype=int, otherwise indexing fails
        in the win search when we try to use float indexes.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        if dimension is None:
            dimension = 0
            return self._get_search_directions(playing_grid=playing_grid,
                                               array_list=[np.array([1], dtype=int)], dimension=dimension + 1)
        elif dimension == np.ndim(playing_grid):
            return array_list
        else:
            new_array_list = []
            for arr in array_list:
                same_array_in_higher_d = np.concatenate((arr, np.array([0], dtype=int)))
                new_array_list.append(same_array_in_higher_d)

                new_array_one = np.concatenate((arr, np.array([1])))
                new_array_list.append(new_array_one)

                new_array_minus_one = np.concatenate((arr, np.array([-1])))
                new_array_list.append(new_array_minus_one)

            # Also add on the nth dimensional unit vector
            unit_array_nth_dim = np.zeros(dimension + 1, dtype=int)
            unit_array_nth_dim[dimension] = 1
            new_array_list.append(unit_array_nth_dim)
            return self._get_search_directions(playing_grid=playing_grid,
                                               array_list=new_array_list, dimension=dimension + 1)

    def _encode_board_as_string(self) -> str:
        """Method that converts the numpy array board into a human readable string"""
        element_wise_int_to_str_func = np.vectorize(
            lambda mark: BoardMarking(mark).name if mark != 0 else BoardString.EMPTY.value)
        np_array_of_strings = element_wise_int_to_str_func(self.playing_grid)
        array_string = np.array2string(np_array_of_strings, separator=BoardString.SEPARATOR.value)
        return array_string

    @staticmethod
    def _decode_board_from_string(string_rep: str) -> np.ndarray:
        pass

    ##########
    # This is a whole board search, i.e. is naive to where the last move was played, and thus is only used
    # when this information is not available
    ##########
    def _whole_board_search(self, playing_grid: np.ndarray = None) -> bool:
        """
        Method to check whether or not the playing_grid has reached a winning state.
        Note that the search will stop as soon as a win is found (i.e. not check subsequent arrays in the list).
        However, all rows are checked first, then verticals etc. could test the impact of a random shuffle on speed.

        Parameters: playing_grid, so that this can be re-used in the minimax ai

        Returns:
        bool: True if a player has won, else false
        win_orientation: The orientation of a winning streak, if any
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
    def _search_array_list_for_win(self, array_list: list[np.ndarray]) -> bool:
        """
        Searches a list of numpy arrays for an a of consecutive markings (1s or -1s), representing a win.

        Each section of length self.win_length is convoluted with an a of ones of length self.win_length.
        i.e. the sum of each section of each a of length self.win_length is taken, because the playing_grid is
        1s and -1s.
        The algorithm then checks if the sum of any sections is at least the required winning streak length.
        """
        for array in array_list:
            convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
            # "valid" kwarg means only where the np.ones a fully overlaps with the row gets calculated
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # Diagonals contains a winning a
        return False  # The algorithm has looped over all south-east diagonals and not found any winning boards

    def _get_row_arrays(self, playing_grid: np.ndarray = None) -> list[np.ndarray]:
        """
        Parameters: playing_grid, so that this can be re-used for minimax
        Returns: a list of the row arrays on the playing grid
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        row_array_list = [playing_grid[row_index] for row_index in range(0, self.game_rows_m)]
        return row_array_list

    def _get_col_arrays(self, playing_grid: np.ndarray = None) -> list[np.ndarray]:
        """
        Parameters: playing_grid, so that this can be re-used for minimax
        Returns: a list of the row arrays on the playing grid
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        col_array_list = [playing_grid[:, col_index] for col_index in range(0, self.game_cols_n)]
        return col_array_list

    def _get_south_east_diagonal_arrays(self, playing_grid: np.ndarray = None) -> list[np.ndarray]:
        """
        Method to extract the south_east diagonals of sufficient length from the playing grid
        The first element in the diagonal_offset_list is the diagonals in the lower triangle and leading diagonal (of
        at least length self.win_length), the second element is those in the upper triangle

        Parameters:
        __________
        playing_grid - so that this method can be re-used to check for north east diagonals too, and in the minimax ai

        Returns:
        __________
        A list of the south east diagonal arrays on the playing grid, of length at least self.win_length.
        i.e. south east diagonal arrays too short to contain a winning streak are intentionally excluded, to avoid
        being searched unnecessarily.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        diagonal_offset_list = list(range(-(self.game_rows_m - self.win_length_k), 0)) + list(
            range(0, self.game_cols_n - self.win_length_k + 1))
        diagonal_array_list = [np.diagonal(playing_grid, offset) for offset in diagonal_offset_list]
        return diagonal_array_list

    def _get_north_east_diagonal_arrays(self, playing_grid: np.ndarray = None) -> list[np.ndarray]:
        """
        Method to extract the north_east diagonals of sufficient length from the playing grid

        Parameters:
        ----------
        Takes the south-east diagonals of the playing_grid flipped upside down - does reverse the order of the arrays
        in that the bottom row becomes the top, but otherwise does not affect the length of a win.

        Returns:
        __________
        A list of the north east diagonal arrays on the playing grid, of length at least self.win_length.
        Note they are north east because the playing_grid has been flipped upside down, so reading along a 1D a
        generated by this method would represent travelling north east on the playing grid.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        return self._get_south_east_diagonal_arrays(playing_grid=np.flipud(playing_grid))
