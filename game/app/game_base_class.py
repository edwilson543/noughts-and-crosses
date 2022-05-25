from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
import numpy as np
from typing import Optional, Union
from dataclasses import dataclass

#  TODO use a data class to carry the attributes for this and all subclasses


@dataclass(frozen=False)
class NoughtsAndCrossesParameters:
    """Dataclass storing all the non-default parameters for the Noughts and Crosses game."""
    game_rows_m: int
    game_cols_n: int
    win_length_k: int
    player_x: Player
    player_o: Player
    starting_player: GameValue


class NoughtsAndCrosses:
    """Base class to reflect the game play of a noughts and crosses game."""

    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue,
                 draw_count: int = 0):
        self.game_rows_m = game_rows_m
        self.game_cols_n = game_cols_n
        self.playing_grid = np.zeros(shape=(game_rows_m, game_cols_n))
        self.win_length_k = win_length_k
        self.pos_player = pos_player
        self.neg_player = neg_player
        self.starting_player = starting_player
        self.draw_count = draw_count

    def choose_starting_player(self, player_name: Optional[str], random: bool = True) -> None:
        """Method to allow manual choice of who goes first."""
        if random:
            self.starting_player = np.random.choice([-1, 1])
        elif player_name == self.pos_player.name:
            self.starting_player = self.pos_player.active_symbol.value  # this will be 1
        elif player_name == self.pos_player.name:
            self.starting_player = self.pos_player.active_symbol.value  # this will be -1
        else:
            raise ValueError("Attempted to call choose_starting_player method non-randomly but with a player_name"
                             "that did not match either of the players.")

    def get_player_turn(self) -> GameValue:
        """
        Method to determine who's turn it is to mark the board, using sum of the board 1s/-1s and who went first.
        If this is the first turn, a player is randomly selected to go first

        Returns:
        GameValue value (1 or -1) - the piece that will get placed following the next turn. Determined by summing the
        1s and -1s - whoever has placed the most
        """
        board_status = self.playing_grid.sum().sum()
        if board_status != 0:  # The starting player has had one more turn than the other player
            player_turn = -board_status
            return - board_status
        else:
            return self.starting_player

    def mark_board(self, row_index: int, col_index: int) -> None:
        """
        Method to make a new entry on the game board.
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
        """Method to perform the winning board search, and return None or the winning player"""
        if not self.winning_board_search():
            return None
        else:
            previous_mark_made_by = - self.get_player_turn()
            if previous_mark_made_by == self.pos_player.active_symbol.value:
                return self.pos_player
            else:
                return self.neg_player

    def check_for_draw(self) -> bool:
        draw = np.all(self.playing_grid != 0)
        if draw:
            self.draw_count += 1
        return draw

    def reset_game_board(self) -> None:
        """Method to reset the game board"""
        self.playing_grid = np.zeros(shape=(self.game_rows_m, self.game_cols_n))

    ##########
    # Method to do the whole board search
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
        row_arrays: list = self.get_row_arrays()
        col_arrays: list = self.get_col_arrays()
        south_east_diag_arrays: list = self.get_south_east_diagonal_arrays(playing_grid=self.playing_grid)
        north_west_diag_arrays: list = self.get_south_west_diagonal_arrays()
        all_arrays: list = row_arrays + col_arrays + south_east_diag_arrays + north_west_diag_arrays
        any_win: bool = self.search_array_list_for_win(array_list=all_arrays)
        return any_win

    ##########
    #  Methods called in winning_board_search
    ##########

    def search_array_list_for_win(self, array_list: list[np.array]) -> bool:
        """
        Searches a list of numpy arrays for one that contains a win

        Checks all relevant arrays of length at least self.win_length_k, and then convolutes each section of length
        self.win_length_k them with an array of ones i.e. sums each section. Then checks if the sum of any sections is
        at least the length of the array.
        """
        for array in array_list:
            convoluted_array = np.convolve(array, np.ones(self.win_length_k, dtype=int), mode="valid")
            # "valid" kwarg means only where the np.ones array fully overlaps with the row gets calculated
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # Diagonals contains a winning array
        return False  # The algorithm has looped over all south-east diagonals and not found any winning boards

    def get_row_arrays(self) -> list[np.array]:
        row_array_list = [self.playing_grid[row_index] for row_index in range(0, self.game_rows_m)]
        return row_array_list

    def get_col_arrays(self) -> list[np.array]:
        col_array_list = [self.playing_grid[:, col_index] for col_index in range(0, self.game_cols_n)]
        return col_array_list

    def get_south_east_diagonal_arrays(self, playing_grid: np.array) -> list[np.array]:
        """
        Playing grid parameter included so that this method can be re-used to check for south west diagonals too.
        The first element in the diagonal_offset_list is the diagonals in the lower triangle and leading diagonal (of
        at least length self.win_length_k), the second element is those in the upper triangle
        """
        diagonal_offset_list = list(range(-(self.game_rows_m - self.win_length_k), 0)) + \
                               list(range(0, self.game_cols_n - self.win_length_k + 1))
        diagonal_array_list = [np.diagonal(playing_grid, offset) for offset in diagonal_offset_list]
        return diagonal_array_list

    def get_south_west_diagonal_arrays(self) -> list[np.array]:
        """
        Takes the south-east diagonals of the board flipped upside down - does reverse the order of the arrays
        in that the bottom row becomes the top, but otherwise does not affect the length of a win.
        """
        return self.get_south_east_diagonal_arrays(playing_grid=np.flipud(self.playing_grid))
