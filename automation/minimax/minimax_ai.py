""""Subclass of the noughts and crosses game that implements the minimax algorithm"""

from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from automation.minimax.terminal_board_scores import TerminalScore
import numpy as np
from typing import List
from random import shuffle
import math


# CURRENTLY minimax is slow for games bigger than 3x3, even with the alpha beta pruning.
# TODO Investigate the below ideas to speed it up
# Introduce a max search depth
# Profile the algorithm with cProfile, set up and automatic game runner which doesn't use the GUI
# Investigate whether implementing caching could help
# Leverage symmetry early on in the game - symmetric branches are strategically equivalent, so if we've already tested
# one, don't need to check rest of equivalence class. (This could come immediately after marking the grid copy).
# This could be done by tracking number of played turns, and switching off after this. Again, profile it.
# Evaluate boards which aren't in an end-state, say by the number of streak of length win_length_k -1


class NoughtsAndCrossesMinimax(NoughtsAndCrosses):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0):
        """Note that the maximising_player is the player that the minimax ai will play as"""
        super().__init__(setup_parameters, draw_count)

    def get_minimax_move(self, last_played_index: np.array = None, playing_grid: np.array = None,
                         search_depth: int = 0, maximisers_move: bool = True,
                         alpha: int = -math.inf, beta: int = math.inf) -> (int, np.ndarray):
        # TODO update docstring
        """
        Parameters:
        ----------
        last_played_index/last_played_col: The row / column that the last board marking was made in. This is included
        so that the win search algorithm (_quick_win_search) only searches the relevant part of the board, speeding
        things up a fair bit. These are defaulted because the minimax only evaluates moves it makes itself, so never
        takes in an external 'last played move' - such a parameter may be a future way to speed it up though.

        playing_grid: The playing grid that is being searched. Note that we can't just used the instance attribute
        playing_grid as this gets altered throughout the searching by testing different game trees.

        search_depth: The depth at which we are searching relative to the current status of the playing_grid

        maximisers_move: T/F depending on whether we are call this function to maximise or minimise the value

        alpha: The best (highest) value the maximiser can already guarantee at the given search depth or above.
        There is therefore no point searching further into game trees where the maximiser CANNOT force a higher value
        than alpha, so on discovering a branch during the maximiser's turn where one of the leaf node values is higher
        than alpha, alpha is updated, and the branch is 'pruned' if the minimiser can guarantee a lower value
        (beta <= alpha).
        Default of -inf (first call) so it can only be improved on.

        beta: The best (lowest) value the minimiser can already guarantee at the given search depth or above.
        This is analogous to alpha - there is no point searching game trees where the minimiser cannot force a lower
        value than beta, so on discovering that a leaf node has a lower value than beta, beta is updated, and the branch
        is pruned if the maximiser can guarantee a higher value (alpha >= beta).
        Default of +inf (first call) so it can only be improved on.

        Returns: (int, np.array)
        __________
        int -  In this case the recursion has reached a board of terminal state, this is the score of that board to the
        maximising player (score). These values are then passed up the game tree, to determine what move the maximiser
        should take, hence an int (min_score/max_score) is returned for each recursion

        np.array - when the board has not reached maximum depth - it returns the move leading to the optimal score,
        assuming the maximiser always maximises and the minimiser always minimises the static evaluation function.
        This is the best move for whichever player's turn is next.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        # Checks for a terminal state (win or draw)
        if last_played_index is not None:
            game_has_been_won, _ = self.win_check_and_location_search(
                get_win_location=False,
                playing_grid=playing_grid,
                last_played_index=last_played_index)
        else:  # This is the first call to minimax from the active game state, so there is no last_played_index/col
            game_has_been_won = False

        game_has_been_drawn = self.check_for_draw(playing_grid=playing_grid)

        # Evaluate the board in a terminal state from the perspective of the maximising player
        if game_has_been_won:
            winning_player = self.get_winning_player(winning_game=game_has_been_won, playing_grid=playing_grid)
            score = self._evaluate_board_to_maximising_player(
                playing_grid=playing_grid, search_depth=search_depth, winning_player=winning_player)
            return score, None
        elif game_has_been_drawn:
            score = self._evaluate_board_to_maximising_player(
                playing_grid=playing_grid, search_depth=search_depth, draw=game_has_been_drawn)
            return score, None

        elif maximisers_move:
            max_score = -math.inf  # Initialise as -inf so that the score can only be improved upon
            best_move = None
            for move_option in self._get_available_cell_indices(playing_grid=playing_grid):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(marking_index=move_option, playing_grid=playing_grid_copy)
                potential_new_max, _ = self.get_minimax_move(  # call minimax recursively until we hit end-state boards
                    last_played_index=move_option, playing_grid=playing_grid_copy,
                    search_depth=search_depth + 1, maximisers_move=not maximisers_move,
                    alpha=alpha, beta=beta)
                # 'not maximisers_move' is to indicate that when minimax is next called, it's the other player's go
                if potential_new_max > max_score:
                    max_score = potential_new_max
                    best_move = move_option
                alpha = max(alpha, potential_new_max)
                if beta <= alpha:
                    break  # No need to consider this game branch any further, as minimiser will avoid it
            return max_score, best_move

        else:  # minimisers move - they want to pick the game tree that minimises the score to the maximiser
            min_score = math.inf  # Initialise as +inf so that score can only be improved upon
            best_move = None
            for move_option in self._get_available_cell_indices(playing_grid=playing_grid):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(marking_index=move_option, playing_grid=playing_grid_copy)
                potential_new_min, _ = self.get_minimax_move(
                    last_played_index=move_option, playing_grid=playing_grid_copy,
                    search_depth=search_depth + 1, maximisers_move=not maximisers_move,
                    alpha=alpha, beta=beta)
                if potential_new_min < min_score:
                    min_score = potential_new_min
                    best_move = move_option
                beta = min(beta, potential_new_min)
                if beta <= alpha:
                    break  # No need to consider game branch any further, maximiser will just avoid it
            return min_score, best_move

    def _evaluate_board_to_maximising_player(self, playing_grid: np.array, search_depth: int,
                                             winning_player: Player | None = None, draw: bool | None = None) -> int:
        """
        Static evaluation function for a playing_grid at the bottom of the minimax search tree, from the perspective
        of the maximising player.
        Note that get_minimax_move() is only ever called for who's go it is next, i.e. the player to maximise for
        is not specified. Therefore, we need to know who's turn it is to mark the board, which is maintained in this
        method through the self.get_player_turn() with the default argument for playing_grid.

        Parameters:
        __________
        playing_grid: the board active IN THE RECURSION TREE

        search_depth: the depth in the search tree of the playing_grid scenario that we are evaluating. This is included
        as a parameter so that winning boards deep in the search tree can be penalised, and losing boards high up
        in the search tree can be favoured, to minimise search depth.

        winning_player: None if there is a draw, or the winning Player object if there is a winner.
        This and the draw parameter are included to avoid having to call the game search method twice.

        draw: whether or not the board is in a draw state

        Notes: the maximising player is taken as the current player's turn - minimax in this app is only ever called
        for the current player's turn.
        """
        if (winning_player is not None) and \
                winning_player.marking.value == self.get_player_turn():  # If end state winner is player AI wants to win
            # Note that we don't use the playing_grid_copy, because we want the turn of the player on the actual grid,
            # not on the copy grid
            return TerminalScore.MAX_WIN.value - search_depth
        elif (winning_player is not None) and \
                winning_player.marking.value == - self.get_player_turn():
            return TerminalScore.MAX_LOSS.value + search_depth
        elif self.check_for_draw(playing_grid=playing_grid):
            return TerminalScore.DRAW.value - search_depth
            # Could test the relative speed of determining whether draws will be reached ahead of a full board
        else:
            raise ValueError("Attempted to evaluate a playing_grid scenario that was not terminal.")

    @staticmethod
    def _get_available_cell_indices(playing_grid: np.array) -> List[np.ndarray]:
        """
        Method that looks at where the cells on the playing_grid are unmarked and returns a list (in a random order) of
        the index of each empty cell. This is the iterator for the minimax method.

        Parameters: playing_grid - this method is called on copies of the playing board, not just the playing board

        Returns: List of the indexes which are available, as numpy arrays.
        """
        available_cell_index_list = [index for index in np.argwhere(playing_grid == 0)]
        shuffle(available_cell_index_list)
        return available_cell_index_list
