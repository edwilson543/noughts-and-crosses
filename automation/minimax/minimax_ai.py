""""Subclass of the noughts and crosses game that implements the minimax algorithm"""

from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from automation.minimax.terminal_board_scores import TerminalScore
import numpy as np
from typing import Tuple, List
from random import shuffle
import math

# todo test effectiveness when a max search depth is introduced -
# currently pretty slow for big games and early on in the game
# TODO test a search algorithm only searching relative to last move made for a win - only really relevant if after
# profiling the algorithm, we know how much of the time is spent profiling
# TODO implement caching


class NoughtsAndCrossesMinimax(NoughtsAndCrosses):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0):
        """Note that the maximising_player is the player that the minimax ai will play as"""
        super().__init__(setup_parameters, draw_count)

    def get_minimax_move(self, playing_grid: np.array = None, search_depth: int = 0, maximisers_move: bool = True,
                         alpha: int = -math.inf, beta: int = math.inf) -> (int, Tuple[int, int]):
        """
        Parameters:
        ----------
        playing_grid: The playing grid that is being searched. Note that we can't just used the instance attribute
        playing_grid as this gets altered throughout the searching by testing different game trees.

        search_depth: The depth at which we are searching relative to the current status of the playing_grid

        maximisers_move: T/F depending on whether we are call this function to maximise or minimise the value

        alpha: The value the maximiser can already guarantee at the given search depth or above - i.e. there is
        no point searching game trees where the minimiser is able to guarantee a lower value than alpha, so on
        discovering a branch on the minimiser's turn where one of the first values is lower than this it is
        'pruned' meaning it's not fully searched. Default of -inf (first call) so it can only be improved on.

        beta: The value the minimiser can already guarantee at the given search depth or above - analogous ot alpha.
        Default of +inf (first call) so it can only be improved on.

        Returns: Union[int, Tuple[int, int]].
        __________
        int when the first if statement passes. In this case the recursion has reached a board of terminal state as
        so just evaluates it

        Tuple[int, int] when the board has not reached maximum depth - it returns the move leading to the optimal score,
        assuming the maximiser always maximises and the minimiser always minimises the static evaluation function.
        This is the best move for whichever player's turn is next.
        """
        if playing_grid is None:
            playing_grid = self.playing_grid

        winning_player = self.get_winning_player(playing_grid=playing_grid)
        draw = self.check_for_draw(playing_grid=playing_grid)
        if (winning_player is not None) or draw:  # Will be called once the recursion reaches a terminal state
            return self.evaluate_board_to_maximising_player(playing_grid=playing_grid, search_depth=search_depth,
                                                            winning_player=winning_player, draw=draw), None

        elif maximisers_move:
            max_score = -math.inf  # Initialise as -inf so that the score can only be improved upon
            best_move = None
            for move_option in self.get_available_cell_indices(playing_grid=playing_grid):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(row_index=move_option[0], col_index=move_option[1], playing_grid=playing_grid_copy)
                potential_new_max, _ = self.get_minimax_move(  # call minimax recursively until we hit end-state boards
                    playing_grid=playing_grid_copy, search_depth=search_depth + 1, maximisers_move=not maximisers_move,
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
            for move_option in self.get_available_cell_indices(playing_grid=playing_grid):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(row_index=move_option[0], col_index=move_option[1], playing_grid=playing_grid_copy)
                potential_new_min, _ = self.get_minimax_move(
                    playing_grid=playing_grid_copy, search_depth=search_depth + 1, maximisers_move=not maximisers_move,
                    alpha=alpha, beta=beta)
                if potential_new_min < min_score:
                    min_score = potential_new_min
                    best_move = move_option
                beta = min(beta, potential_new_min)
                if beta <= alpha:
                    break  # No need to consider game branch any further, maximiser will just avoid it
            return min_score, best_move

    def evaluate_board_to_maximising_player(self, playing_grid: np.array, search_depth: int,
                                            winning_player: Player, draw: bool) -> int:
        """
        Static evaluation function for a playing_grid at the bottom of the minimax search tree, from the perspective
        of the maximising player.

        Parameters:
        __________
        playing_grid: the board active IN THE RECURSION TREE

        search_depth: the depth in the search tree of the playing_grid scenario that we are evaluating. This is included
        as a parameter so that winning boards deep in the search tree can be penalised, and losing boards high up
        in the search tree can be favoured, to minimise search depth.

        winning_player: None if there is a draw, or a Player if there is a winner. This and the draw parameter are
        included to avoid having to call the game search method twice.

        draw: whether or not the board is in a draw state
        """
        if (winning_player is not None) and\
                winning_player.marking.value == self.get_player_turn(playing_grid=self.playing_grid):
            return TerminalScore.MAX_WIN.value - search_depth
        elif (winning_player is not None) and\
                winning_player.marking.value == - self.get_player_turn(playing_grid=self.playing_grid):
            return TerminalScore.MAX_LOSS.value + search_depth
        elif self.check_for_draw(playing_grid=playing_grid):
            return TerminalScore.DRAW.value
            # Could also see the impact of penalising slow draws, if these can be determined
        else:
            raise ValueError("Attempted to evaluate a playing_grid scenario that was not terminal.")

    @staticmethod
    def get_available_cell_indices(playing_grid: np.array) -> List[Tuple[int, int]]:
        """
        Method that looks at where the cells on the playing_grid are unmarked and returns a list (in a random order) of
        the index of each empty cell. This is the iterator for the minimax method.
        Parameters: playing_grid - this method is called on copies of the playing board, not just the playing board
        """
        available_cell_index_list = [tuple(index) for index in np.argwhere(playing_grid == 0)]
        shuffle(available_cell_index_list)
        return available_cell_index_list

    # def is_terminal(self, playing_grid: np.array) -> bool:
    #     """
    #     Method that indicates whether or not a certain state of the playing_grid is terminal or not.
    #     Parameters: playing_grid - this method is called on copies of the playing board, not just the playing board
    #     """
    #     return (self.get_winning_player(playing_grid=playing_grid) is not None) or \
    #            (self.check_for_draw(playing_grid=playing_grid))
