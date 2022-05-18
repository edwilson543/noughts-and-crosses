from app.player_base_class import Player
from constants.game_constants import GameValue
import numpy as np

class NoughtsAndCrosses:
    """Base class to reflect the game play of a noughts and crosses game."""
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 player_o: Player,
                 player_x: Player,
                 starting_player: GameValue=GameValue.X):
        self.game_rows_m = game_rows_m
        self.game_cols_n = game_cols_n
        self.playing_grid = np.zeros((game_rows_m, game_cols_n))
        self.win_length_k = win_length_k
        self.player_o = player_o
        self.player_x = player_x
        self.starting_player = starting_player

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
            All rows are looped over and an array of length self.win_length_k containing just 1s is dot producted with
            the elements covered by that window. This works because the board is populated with -1, 0 and 1.
            """
            convoluted_array = np.convolve(playing_grid[row_index],
                                           np.ones(self.win_length_k, dtype=int),
                                           mode="same") # same key word prevents including first and last index
            max_consecutive = max(abs(convoluted_array))
            if max_consecutive == self.win_length_k:
                return True  # The row contains a winning row
            else:
                continue
        return False  # The algorithm has looped over all rows and not found any winning boards

    def check_for_south_east_diagonal_win(self, playing_grid: np.array) -> bool:
        pass

