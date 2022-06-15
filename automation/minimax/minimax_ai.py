""""Subclass of the noughts and crosses game that implements the minimax algorithm"""

# Standard library imports
import functools
import time
from typing import List, Tuple
from random import shuffle
import math

# Third party imports
import numpy as np

# Local application imports
from automation.minimax.constants.terminal_board_scores import TerminalScore
from automation.minimax.constants.iterative_deepening_constants import IterativeDeepening
from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from utils import lru_cache_hashable

# Could use caching here as for the win_search - would want to cache on playing_grid, search_depth,
# maximisers_move. Could then also use symmetry high up in the search


class NoughtsAndCrossesMinimax(NoughtsAndCrosses):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters):
        """Note that the maximising_player is the player that the minimax ai will play as"""
        super().__init__(setup_parameters)

    def get_minimax_move_iterative_deepening(self) -> Tuple[int, np.ndarray | None]:
        """
        Method that calls get_minimax_move_at_max_search_depth at iteratively deeper maximum search depths, until
        the maximum search time has elapsed.
        Returns: as for get_minimax_move_at_max_search_depth
        """
        search_start_time = time.perf_counter()
        current_max_score = - math.inf
        current_best_move = None
        for iterative_search_depth in range(1, IterativeDeepening.max_search_depth.value + 1):
            max_score, best_move = self.get_minimax_move_at_max_search_depth(
                search_start_time=search_start_time, max_search_depth=iterative_search_depth)
            if max_score > current_max_score:  # Could call max to set the score, need a condition for setting move
                current_best_move = best_move
                current_max_score = max_score
            if time.perf_counter() - search_start_time > IterativeDeepening.max_search_seconds.value:
                return current_max_score, current_best_move
            if max_score > TerminalScore.DRAW.value:
                # TODO improve on this
                # If this is the case, at the current depth we found a win, so we won't find a better score at a further
                # depth, because of the simple scoring function that is: winning_score - search_depth
                return current_max_score, current_best_move
        return current_max_score, current_best_move

    def get_minimax_move_at_max_search_depth(self,
                                             max_search_depth: int,
                                             search_start_time: float,
                                             last_played_index: None | np.ndarray = None,
                                             playing_grid: None | np.ndarray = None,
                                             search_depth: int = 0,
                                             maximisers_move: bool = True,
                                             alpha: int = -math.inf,
                                             beta: int = math.inf) -> Tuple[int, np.ndarray | None]:
        """
        Parameters:
        ----------
        max_search_depth: The search depth at which the call to this method must stop searching any further and return
        the best move currently assessed.

        search_start_time: The time when the call to get_minimax_move_iterative_deepening() was first made - this is
        passed so the search stops if max time has elapsed. This is checked both within each depth (by this method)
        and when changing depth (the iterative_deepening call to this method, above)

        last_played_index/last_played_col: The row / column that the last board marking was made in. This is included
        so that the win search algorithm only searches the relevant part of the board, speeding
        things up a fair bit. These are defaulted because minimax here only evaluates moves it makes itself, so never
        takes in an external 'last played move' - such a parameter may be a future way to speed it up by only
        considering the most relevant part of the game board.

        playing_grid: The playing grid that is being searched. Note that we can't just used the instance attribute
        playing_grid as this gets altered throughout the searching by testing different game trees.

        search_depth: The depth at which we are searching relative to the current status of the playing_grid

        maximisers_move: T/F depending on whether the call to this method is to maximise or minimise the score

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

        Returns: Tuple[int, np.ndarray]
        __________
        int -  In this case the recursion has reached a board of terminal state, this is the score of that board to the
        maximising player (score). These values are then passed up the game tree, to determine what move the maximiser
        should take, hence an int (min_score/max_score) is returned for each recursion

        np.ndarray - when the board has not reached maximum depth - it returns the move leading to the optimal score,
        assuming the maximiser always maximises and the minimiser always minimises the static evaluation function.
        This is the best move for whichever player's turn is next.
        """
        # None parameter for playing_grid is only passed in primary (non-recursive) calls
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

        # Evaluate the board in a terminal state from the perspective of the maximising player
        if game_has_been_won:
            winning_player = self.get_winning_player(winning_game=game_has_been_won, playing_grid=playing_grid)
            score = self._evaluate_terminal_board_to_maximising_player(
                search_depth=search_depth, winning_player=winning_player)
            return score, None
        elif self.check_for_draw(playing_grid=playing_grid):
            score = self._evaluate_terminal_board_to_maximising_player(
                search_depth=search_depth, draw=True)
            return score, None

        # Check whether our iterative deepening criteria have been exhausted:
        elif time.perf_counter() - search_start_time > IterativeDeepening.max_search_seconds.value:
            # Although this exit criteria is also included in the iterative loop, a given depth may also take too long
            score = self._evaluate_non_terminal_board_to_maximising_player(
                playing_grid=playing_grid, search_depth=search_depth)
            return score, None
        elif search_depth == max_search_depth:
            score = self._evaluate_non_terminal_board_to_maximising_player(
                playing_grid=playing_grid, search_depth=search_depth)
            return score, None

        # Otherwise, we need to evaluate the max/min score attainable and associated move
        elif maximisers_move:
            max_score = -math.inf  # Initialise as -inf so that the score can only be improved upon
            best_move = None
            for move_option in self._get_available_cell_indices(
                    playing_grid=playing_grid, last_index=last_played_index):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(marking_index=move_option, playing_grid=playing_grid_copy)
                potential_new_max, _ = self.get_minimax_move_at_max_search_depth(  # call minimax recursively
                    search_start_time=search_start_time, max_search_depth=max_search_depth,
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
            for move_option in self._get_available_cell_indices(
                    playing_grid=playing_grid, last_index=last_played_index):
                playing_grid_copy = playing_grid.copy()
                self.mark_board(marking_index=move_option, playing_grid=playing_grid_copy)
                potential_new_min, _ = self.get_minimax_move_at_max_search_depth(  # call minimax recursively
                    search_start_time=search_start_time, max_search_depth=max_search_depth,
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

    def _evaluate_terminal_board_to_maximising_player(self, search_depth: int,
                                                      winning_player: Player | None = None,
                                                      draw: bool | None = None) -> int:
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
        for the current player's turn. Hence we just call get_player_turn with no playing_grid argument, because we
        want to know the turn of the player in the live game.
        """
        if (winning_player is not None) and \
                winning_player.marking.value == self.get_player_turn():
            return TerminalScore.MAX_WIN.value - search_depth
        elif (winning_player is not None) and \
                winning_player.marking.value == - self.get_player_turn():  # Note minus here (i.e. minimax would lose)
            return TerminalScore.MAX_LOSS.value + search_depth
        elif draw:
            return TerminalScore.DRAW.value - search_depth
            # Could test the relative speed of determining whether draws will be reached ahead of a full board
        else:
            raise ValueError("Attempted to evaluate a playing_grid scenario that was not terminal.")

    @staticmethod
    def _evaluate_non_terminal_board_to_maximising_player(playing_grid: np.ndarray, search_depth: int) -> int:
        """
        Method to evaluate the playing board from the maximiser's perspective, when the algorithm has been forced
        to end because the maximum search depth is reached, or the maximum search time has elapsed.
        """
        # TODO can think of something more clever to do here
        # Need to make this a function of the other player's max win streak
        # As the only way the player knows to block is if it leads to a win or draw
        return TerminalScore.NON_TERMINAL.value - search_depth

    def _get_available_cell_indices(self, playing_grid: np.ndarray, last_index: np.ndarray = None) -> List[np.ndarray]:
        """
        Method that looks at where the cells on the playing_grid are unmarked and returns a list of the index of each
        empty cell. This is the iterator for the minimax method.
        If the game has already started, the list is prioritised according to proximity to the previous move.
        A max branching factor is already introduced, which is used to slice the head off the list and only return this

        Parameters:
        playing_grid: this method is called on copies of the playing board, not just the playing board
        last_played_index: where the previous mark was made. Note that this serves the purpose of prioritising which
        available cells to search first - those closest to the player's move

        Returns: List of the indexes which are available, as numpy arrays, up to the max branching factor.

        Notes: tested speed of the key function in the sorted() below using different options, including a lambda.
        The cached partial function currently implemented was the fastest of those tested. A partial function is used
        because the key must be callable. An alternative is to use an inner wrapper in the _available_cell_prioritiser,
        and then return this, but this was also slower.
        """
        available_cell_index_list = [index for index in np.argwhere(playing_grid == 0)]
        shuffle(available_cell_index_list)
        if self.previous_mark_index is None:  # This is the first move of the game
            return available_cell_index_list[:IterativeDeepening.max_branch_factor.value]
        elif last_index is None:  # This is a primary minimax call to minimax
            prioritised_list = sorted(available_cell_index_list,
                                      key=functools.partial(self._available_cell_prioritiser, self.previous_mark_index))
            return prioritised_list[:IterativeDeepening.max_branch_factor.value]
        else:  # Order the list so that we search in order of distance from the last played index
            prioritised_list = sorted(available_cell_index_list,
                                      key=functools.partial(self._available_cell_prioritiser, last_index))
            return prioritised_list[:IterativeDeepening.max_branch_factor.value]

    @staticmethod
    @lru_cache_hashable(maxsize=100000)  # Can be infinite but specified to avoid memory blow up
    def _available_cell_prioritiser(last_played_index: np.ndarray, available_index: np.ndarray) -> float:
        """
        Method to define an order that can be used to sort a list of available empty cells in order of which
        should be searched first.
        This is important as minimax is now against the clock.
        """
        return np.linalg.norm(last_played_index - available_index)

    # TODO specify the cache max sizes somewhere globally, to avoid memory overallocation
