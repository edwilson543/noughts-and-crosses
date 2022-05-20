from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
import numpy as np
from typing import Optional


class NoughtsAndCrosses:
    """Base class to reflect the game play of a noughts and crosses game."""

    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue = None):
        self.game_rows_m = game_rows_m
        self.game_cols_n = game_cols_n
        self.playing_grid = np.zeros((game_rows_m, game_cols_n))
        self.win_length_k = win_length_k
        self.pos_player = pos_player
        self.neg_player = neg_player
        self.starting_player = starting_player

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
        if board_status != 0:  # Game has already started
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

    def winning_board_search(self) -> bool:
        """
        Method to check whether or not the board has reached a winning state.
        Returns:
        -------
        bool: True if a player has won, else false

        Note there is no need to return the winning player, as this is implied by the starting_player attribute.
        """
        horizontal_win: bool = self.check_for_horizontal_win(playing_grid=self.playing_grid)
        vertical_win: bool = self.check_for_horizontal_win(playing_grid=self.playing_grid.transpose())
        south_east_win: bool = self.check_for_south_east_diagonal_win(playing_grid=self.playing_grid)
        south_west_win: bool = self.check_for_south_east_diagonal_win(playing_grid=self.playing_grid.transpose())
        any_win: bool = horizontal_win + vertical_win + south_east_win + south_west_win
        return any_win

    ##########
    #  Methods called when searching for winning lines
    ##########
    def check_for_horizontal_win(self, playing_grid: np.array) -> bool:
        """
        Method to check whether a horizontal win has been achieved on the game board.

        Parameters:
        -----------
        playing_grid: This is included as a parameter rather than accessing the playing_grid attribute directly so that
        the method can also be used to check for vertical wins by entering the transpose of the board.

        Returns:
        --------
        bool: T/F depending on whether the entered playing_grid exhibits a horizontal win
        """
        for row_index in range(0, self.game_rows_m):
            """
            All rows are looped over and an array of length self.win_length_k containing just 1s is dot-producted with
            the elements covered by that window. This works because the board is populated with -1, 0 and 1.
            """
            convoluted_array = np.convolve(playing_grid[row_index],
                                           np.ones(self.win_length_k, dtype=int),
                                           mode="valid")  # same key word prevents including first and last index
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # The row contains a winning row
            else:
                continue
        return False  # The algorithm has looped over all rows and not found any winning boards

    def check_for_south_east_diagonal_win(self, playing_grid: np.array) -> bool:
        """Use numpy.diag() method"""
        pass
