from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking, StartingPlayer
import numpy as np
from typing import Union
from dataclasses import dataclass


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
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0):
        self.game_rows_m = setup_parameters.game_rows_m
        self.game_cols_n = setup_parameters.game_cols_n
        self.win_length_k = setup_parameters.win_length_k
        self.player_x = setup_parameters.player_x
        self.player_o = setup_parameters.player_o
        self.starting_player_value = self.get_starting_player(
            starting_player_value=setup_parameters.starting_player_value)
        self.draw_count = draw_count
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n))

    ##########
    # Methods that are a part of the core game play flow
    ##########
    @staticmethod
    def get_starting_player(starting_player_value: StartingPlayer) -> BoardMarking:
        """
        Method to allow choice of who goes first, or to be randomly selected.
        Note that the starting player is carried as either 1 or -1 (which corresponds with the BoardMarking Enum)
        """
        if starting_player_value == StartingPlayer.RANDOM.value:
            return np.random.choice([BoardMarking.X.value, BoardMarking.O.value])
        elif starting_player_value == StartingPlayer.PLAYER_X.value:
            return BoardMarking.X.value
        elif starting_player_value == StartingPlayer.PLAYER_O.value:
            return BoardMarking.O.value
        else:
            raise ValueError("Attempted to call choose_starting_player method non-randomly but with a player_name"
                             "that did not match either of the players.")

    def get_player_turn(self) -> BoardMarking:
        """
        Method to determine who's turn it is to mark the board, using sum of the board 1s/-1s.
        If the sum is zero then both player's have had an equal number of turns, and therefore it's the starting
        player's turn. Otherwise, the starting player has had an extra go, so it's the other player's turn.

        Returns:
        BoardMarking value (1 or -1) - the piece that will get placed following the next turn.
        """
        board_status = self.playing_grid.sum().sum()
        if board_status != 0:  # The starting player has had one more turn than the other player
            player_turn = -board_status
            return - board_status
        else:
            return self.starting_player_value

    def mark_board(self, row_index: int, col_index: int) -> None:
        """
        Method to make a new entry on the game board. Note that there is no opportunity to mark out of turn, because the
        get_player_turn method is called within this method.
        Parameters:
        Row/col index - the index of the playing_grid where the mark will be made
        Returns:
        None
        Outcomes:
        If the cell is empty, a mark is made, else a value error is raised
        """
        if self.playing_grid[row_index, col_index] == 0:
            marking = self.get_player_turn()
            self.playing_grid[row_index, col_index] = marking
        else:
            raise ValueError(f"mark_board attempted to mark non-empty cell at {row_index, col_index}.")

    def get_winning_player(self) -> Union[None, Player]:
        """
        Method to perform the winning board search, and return None or the winning player,
        depending on if there's a winning player.
        """
        if not self.winning_board_search():
            return None
        else:
            previous_mark_made_by = - self.get_player_turn()
            if previous_mark_made_by == BoardMarking.X.value:
                return self.player_x
            else:
                return self.player_o

    def check_for_draw(self) -> bool:
        """
        Method that checks whether or not the board has reached a stalemate.
        This is currently naive in that it just checks for a full board - a draw may in fact have been guaranteed sooner
        than the board being full.
        #  TODO think about how to address this
        """
        draw = np.all(self.playing_grid != 0)
        if draw:
            self.draw_count += 1
        return draw

    def reset_game_board(self) -> None:
        """Method to reset the game board - replaces all entries in the playing_grid with a zero"""
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n))

    # Lower level methods that are needed for the core game flow
    ##########
    # Search algorithm for the whole board win search
    ##########
    def winning_board_search(self) -> bool:
        """
        Method to check whether or not the board has reached a winning state.
        Note that the search will stop as soon as a win is found (i.e. not check subsequent arrays in the list).
        However, all rows are checked first, then verticals etc. so # todo check the impact of adding a random shuffle

        Returns:
        -------
        bool: True if a player has won, else false
        """
        row_arrays: list = self._get_row_arrays()
        col_arrays: list = self._get_col_arrays()
        south_east_arrays: list = self._get_south_east_diagonal_arrays(playing_grid=self.playing_grid)
        north_east_arrays: list = self._get_north_east_diagonal_arrays()
        all_arrays: list = row_arrays + col_arrays + south_east_arrays + north_east_arrays
        any_win: bool = self.search_array_list_for_win(array_list=all_arrays)
        return any_win

    #  Methods called in winning_board_search
    def search_array_list_for_win(self, array_list: list[np.array]) -> bool:
        """
        Searches a list of numpy arrays for an array of consecutive markings (1s or -1s), representing a win.

        Each section of length self.win_length_k is convoluted with an array of ones of length self.win_length_k.
        i.e. the sum of each section of each array of length self.win_length_k is taken, because the board is 1s and -1s
        The algorithm then checks if the sum of any sections is at least the required winning streak length.
        """
        for array in array_list:
            convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
            # "valid" kwarg means only where the np.ones array fully overlaps with the row gets calculated
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # Diagonals contains a winning array
        return False  # The algorithm has looped over all south-east diagonals and not found any winning boards

    def _get_row_arrays(self) -> list[np.array]:
        """Returns: a list of the row arrays on the playing grid"""
        row_array_list = [self.playing_grid[row_index] for row_index in range(0, self.game_rows_m)]
        return row_array_list

    def _get_col_arrays(self) -> list[np.array]:
        """Returns: a list of the column arrays on the playing grid"""
        col_array_list = [self.playing_grid[:, col_index] for col_index in range(0, self.game_cols_n)]
        return col_array_list

    def _get_south_east_diagonal_arrays(self, playing_grid: np.array) -> list[np.array]:
        """
        Method to extract the south_east diagonals of sufficient length from the playing grid
        The first element in the diagonal_offset_list is the diagonals in the lower triangle and leading diagonal (of
        at least length self.win_length_k), the second element is those in the upper triangle

        Parameters:
        __________
        playing_grid - so that this method can be re-used to check for north east diagonals too.

        Returns:
        __________
        A list of the south east diagonal arrays on the playing grid, of length at least self.win_length_k.
        i.e. south east diagonal arrays too short to contain a winning streak are intentionally excluded, to avoid
        being searched unnecessarily.
        """
        diagonal_offset_list = list(range(-(self.game_rows_m - self.win_length_k), 0)) + list(
            range(0, self.game_cols_n - self.win_length_k + 1))
        diagonal_array_list = [np.diagonal(playing_grid, offset) for offset in diagonal_offset_list]
        return diagonal_array_list

    def _get_north_east_diagonal_arrays(self) -> list[np.array]:
        """
        Method to extract the north_east diagonals of sufficient length from the playing grid

        Takes the south-east diagonals of the board flipped upside down - does reverse the order of the arrays
        in that the bottom row becomes the top, but otherwise does not affect the length of a win.

        Returns:
        __________
        A list of the north east diagonal arrays on the playing grid, of length at least self.win_length_k.
        Note they are north east because the board has been flipped upside down, so reading along a 1D array generated
        by this method would represent travelling north east on the playing grid.
        """
        return self._get_south_east_diagonal_arrays(playing_grid=np.flipud(self.playing_grid))
