from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking, StartingPlayer, WinOrientation
import numpy as np
from typing import Union, List, Tuple
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
        if starting_player_value is None:
            pass
        if starting_player_value == StartingPlayer.RANDOM.value:
            return np.random.choice([BoardMarking.X.value, BoardMarking.O.value])
        elif starting_player_value == StartingPlayer.PLAYER_X.value:
            return BoardMarking.X.value
        elif starting_player_value == StartingPlayer.PLAYER_O.value:
            return BoardMarking.O.value
        else:
            raise ValueError("Attempted to call choose_starting_player method but with a starting_player_value"
                             " that is not in the StartingPlayer Enum.")

    def get_player_turn(self, playing_grid: np.array = None) -> BoardMarking:
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
            player_turn = -board_status
            return - board_status
        else:
            return self.starting_player_value

    def mark_board(self, row_index: int, col_index: int, playing_grid: np.array = None) -> None:
        """
        Method to make a new entry on the game playing_grid. Note that there is no opportunity to mark out of turn,
        because the get_player_turn method is called within this method.
        Parameters:
        Row/col index - the index of the playing_grid where the mark will be made
        Returns:
        None
        Outcomes:
        If the cell is empty, a mark is made, else a value error is raised
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        if playing_grid[row_index, col_index] == 0:
            marking = self.get_player_turn(playing_grid=playing_grid)
            playing_grid[row_index, col_index] = marking
        else:
            raise ValueError(f"mark_board attempted to mark non-empty cell at {row_index, col_index}.")

    def get_winning_player(self, playing_grid: np.array = None) -> Union[None, Player]:
        """
        Method to perform the winning playing_grid search, and return None or the winning player,
        depending on if there's a winning player.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        win, _ = self._winning_board_search(playing_grid=playing_grid)
        if not win:
            return None
        else:
            previous_mark_made_by = - self.get_player_turn(playing_grid=playing_grid)
            if previous_mark_made_by == BoardMarking.X.value:
                return self.player_x
            else:
                return self.player_o

    def check_for_draw(self, playing_grid: np.array = None) -> bool:
        """
        Method that checks whether or not the playing_grid has reached a stalemate.
        This is currently naive in that it just checks for a full playing_grid - a draw may in fact have been
        guaranteed sooner than the playing_grid being full.
        #  TODO think about how to address this

        Parameters: playing_grid, to allow re-use for minimax
        Returns: bool - T/F depending on whether the board has reached a draw
        """
        live_board_check = False  # whether we are checking the actual playing board, or just a copy of it
        if playing_grid is None:
            playing_grid = self.playing_grid
            live_board_check = True
        draw = np.all(playing_grid != 0)
        if draw and live_board_check:
            self.draw_count += 1
        return draw

    def reset_game_board(self) -> None:
        """Method to reset the game playing_grid - replaces all entries in the playing_grid with a zero"""
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n))

    # Lower level methods that are needed for the core game flow
    ##########
    # Search algorithm for the whole playing_grid win search
    ##########
    def _winning_board_search(self, playing_grid: np.array = None) -> (bool, WinOrientation):
        """
        Method to check whether or not the playing_grid has reached a winning state.
        Note that the search will stop as soon as a win is found (i.e. not check subsequent arrays in the list).
        However, all rows are checked first, then verticals etc. so # todo check the impact of adding a random shuffle

        Parameters: playing_grid, so that this can be re-used in the minimax ai

        Returns:
        bool: True if a player has won, else false
        win_orientation: The orientation of a winning streak, if any
        """
        win_orientation = None
        if playing_grid is None:
            playing_grid = self.playing_grid

        if self._search_array_list_for_win(
                array_list=self._get_row_arrays(playing_grid=playing_grid)):
            win_orientation = WinOrientation.HORIZONTAL
        elif self._search_array_list_for_win(
                array_list=self._get_col_arrays(playing_grid=playing_grid)):
            win_orientation = WinOrientation.VERTICAL
        elif self._search_array_list_for_win(
                array_list=self._get_south_east_diagonal_arrays(playing_grid=playing_grid)):
            win_orientation = WinOrientation.SOUTH_EAST
        elif self._search_array_list_for_win(
                array_list=self._get_north_east_diagonal_arrays(playing_grid=playing_grid)):
            win_orientation = WinOrientation.NORTH_EAST
        return (win_orientation is not None), win_orientation

    def win_location_search(self, row_index: int, col_index: int, win_orientation: WinOrientation,
                            playing_grid: np.array = None) -> List[Tuple[int, int]]:
        """
        Method to determine the LOCATION of a win given that we know there is a win.
        The method leverages the fact that we only need to search the intersection of the last move with the board.
        Note this is not used to check for wins, only to determine where they are once we know there is one - hence
        the reason for currently having a separate method.
        # TODO an independent search algorithm could be built like this - that just searches based on last move

        Parameters:
        ----------
        playing_grid - the board
        row_index.col_index - where the last move on the board was made

        Returns:
        ----------
        A list of the indexes corresponding to the winning streak
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        if win_orientation == WinOrientation.HORIZONTAL:
            row_streaks = np.convolve(playing_grid[row_index], np.ones(self.win_length_k, dtype=int), mode="valid")
            win_streak_start_col = int(np.where(abs(row_streaks) == self.win_length_k)[0])
            return [(row_index, win_streak_start_col + k) for k in range(0, self.win_length_k)]
        elif win_orientation == WinOrientation.VERTICAL:
            col_streaks = np.convolve(playing_grid[:, col_index], np.ones(self.win_length_k, dtype=int), mode="valid")
            win_streak_start_row = int(np.where(abs(col_streaks) == self.win_length_k)[0])
            return [(win_streak_start_row + k, col_index) for k in range(0, self.win_length_k)]
        elif win_orientation == WinOrientation.SOUTH_EAST:
            diagonal_offset = col_index - row_index
            diagonal_offset_index = (max(-diagonal_offset, 0), max(diagonal_offset, 0))
            diagonal_array = np.diagonal(playing_grid, offset=diagonal_offset)
            diag_streaks = np.convolve(diagonal_array, np.ones(self.win_length_k, dtype=int), mode="valid")
            win_streak_start_pos = int(np.where(abs(diag_streaks) == self.win_length_k)[0])
            return [(win_streak_start_pos + diagonal_offset_index[0] + k,
                     win_streak_start_pos + diagonal_offset_index[1] + k)
                    for k in range(0, self.win_length_k)]
        elif win_orientation == WinOrientation.NORTH_EAST:
            diagonal_offset = (playing_grid.shape[1] - col_index - 1) - row_index
            diagonal_offset_index = (max(-diagonal_offset, 0), (playing_grid.shape[1] - 1 - max(diagonal_offset, 0)))
            diagonal_array = np.fliplr(playing_grid).diagonal(offset=diagonal_offset)
            diag_streaks = np.convolve(diagonal_array, np.ones(self.win_length_k, dtype=int), mode="valid")
            win_streak_start_pos = int(np.where(abs(diag_streaks) == self.win_length_k)[0])
            return[(win_streak_start_pos + diagonal_offset_index[0] + k,
                    win_streak_start_pos + diagonal_offset_index[1] - k)
                   for k in range(0, self.win_length_k)]
        else:
            raise ValueError("Invalid win_orientation was passed to win_location_search")

    #  Methods called in winning_board_search and quick_search
    def _search_array_list_for_win(self, array_list: list[np.array]) -> bool:
        """
        Searches a list of numpy arrays for an array of consecutive markings (1s or -1s), representing a win.

        Each section of length self.win_length_k is convoluted with an array of ones of length self.win_length_k.
        i.e. the sum of each section of each array of length self.win_length_k is taken, because the playing_grid is
        1s and -1s.
        The algorithm then checks if the sum of any sections is at least the required winning streak length.
        """
        for array in array_list:
            convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
            # "valid" kwarg means only where the np.ones array fully overlaps with the row gets calculated
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # Diagonals contains a winning array
        return False  # The algorithm has looped over all south-east diagonals and not found any winning boards

    def _get_row_arrays(self, playing_grid: np.array = None) -> list[np.array]:
        """
        Parameters: playing_grid, so that this can be re-used for minimax
        Returns: a list of the row arrays on the playing grid
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        row_array_list = [playing_grid[row_index] for row_index in range(0, self.game_rows_m)]
        return row_array_list

    def _get_col_arrays(self, playing_grid: np.array = None) -> list[np.array]:
        """
        Parameters: playing_grid, so that this can be re-used for minimax
        Returns: a list of the row arrays on the playing grid
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        col_array_list = [playing_grid[:, col_index] for col_index in range(0, self.game_cols_n)]
        return col_array_list

    def _get_south_east_diagonal_arrays(self, playing_grid: np.array = None) -> list[np.array]:
        """
        Method to extract the south_east diagonals of sufficient length from the playing grid
        The first element in the diagonal_offset_list is the diagonals in the lower triangle and leading diagonal (of
        at least length self.win_length_k), the second element is those in the upper triangle

        Parameters:
        __________
        playing_grid - so that this method can be re-used to check for north east diagonals too, and in the minimax ai

        Returns:
        __________
        A list of the south east diagonal arrays on the playing grid, of length at least self.win_length_k.
        i.e. south east diagonal arrays too short to contain a winning streak are intentionally excluded, to avoid
        being searched unnecessarily.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        diagonal_offset_list = list(range(-(self.game_rows_m - self.win_length_k), 0)) + list(
            range(0, self.game_cols_n - self.win_length_k + 1))
        diagonal_array_list = [np.diagonal(playing_grid, offset) for offset in diagonal_offset_list]
        return diagonal_array_list

    def _get_north_east_diagonal_arrays(self, playing_grid: np.array = None) -> list[np.array]:
        """
        Method to extract the north_east diagonals of sufficient length from the playing grid

        Parameters:
        ----------
        Takes the south-east diagonals of the playing_grid flipped upside down - does reverse the order of the arrays
        in that the bottom row becomes the top, but otherwise does not affect the length of a win.

        Returns:
        __________
        A list of the north east diagonal arrays on the playing grid, of length at least self.win_length_k.
        Note they are north east because the playing_grid has been flipped upside down, so reading along a 1D array
        generated by this method would represent travelling north east on the playing grid.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid
        return self._get_south_east_diagonal_arrays(playing_grid=np.flipud(playing_grid))
