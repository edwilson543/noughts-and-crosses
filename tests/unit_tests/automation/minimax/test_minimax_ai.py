"""Test to see whether the minimax goes in for the kill when presented the opportunity."""

from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from automation.minimax.terminal_board_scores import TerminalScore
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking, StartingPlayer
import numpy as np
import pytest


class TestMinimaxThreeThreeThree:
    """Class to test the effectiveness of the minimax function on a m,n,k = 3,3,3 game."""
    @pytest.fixture(scope="class")
    def human_player(self):
        return Player(name="Human", marking=BoardMarking.X)

    @pytest.fixture(scope="class")
    def minimax_player(self):
        return Player(name="Minimax", marking=BoardMarking.O)

    @pytest.fixture(scope="class")
    def new_game_parameters(self, human_player, minimax_player):
        """
        A starting player is included so that we aren't missing a non-default arg, however is specified throughout
        testing. Note that if a board configuration is manually specified which implies a starting player different
        to that manually specified, then minimax will fail as it'll try to play for the human.
        """
        return NoughtsAndCrossesEssentialParameters(
            game_rows_m=3,
            game_cols_n=3,
            win_length_k=3,
            player_x=human_player,
            player_o=minimax_player,
            starting_player_value=StartingPlayer.PLAYER_O.value)

    @pytest.fixture(scope="function")
    def new_game_with_minimax_player(self, new_game_parameters):
        return NoughtsAndCrossesMinimax(
            setup_parameters=new_game_parameters,
        )

    def test_minimax_gets_winning_move_bottom_right_row(self, new_game_with_minimax_player):
        """Test that minimax can win in one move when presented opportunity (bottom row win)"""
        new_game_with_minimax_player.starting_player_value = StartingPlayer.PLAYER_O.value
        new_game_with_minimax_player.playing_grid = np.array([
            [BoardMarking.X.value, 0, BoardMarking.X.value],
            [0, 0, 0],
            [BoardMarking.O.value, BoardMarking.O.value, 0]
        ])
        score, minimax_move = new_game_with_minimax_player.get_minimax_move_iterative_deepening()
        assert score == TerminalScore.MAX_WIN.value - 1  # -1 to reflect a search depth of 1 to find the win
        assert np.all(minimax_move == np.array([2, 2]))

    def test_minimax_gets_winning_move_north_east_diagonal(self, new_game_with_minimax_player):
        """Test that minimax can win in one move when presented opportunity (north east diagonal win)"""
        new_game_with_minimax_player.starting_player_value = StartingPlayer.PLAYER_O.value
        new_game_with_minimax_player.playing_grid = np.array([
            [BoardMarking.X.value, 0, BoardMarking.O.value],
            [0, 0, 0],
            [BoardMarking.O.value, BoardMarking.X.value, 0]
        ])
        score, minimax_move = new_game_with_minimax_player.get_minimax_move_iterative_deepening()
        assert score == TerminalScore.MAX_WIN.value - 1  # -1 to reflect a search depth of 1 to find the win
        assert np.all(minimax_move == np.array([1, 1]))

    def test_minimax_makes_blocking_move_middle_left_vertical(self, new_game_with_minimax_player):
        """Test that minimax can win in one move when presented opportunity"""
        new_game_with_minimax_player.starting_player_value = StartingPlayer.PLAYER_X.value
        new_game_with_minimax_player.playing_grid = np.array([
            [BoardMarking.X.value, 0, BoardMarking.O.value],
            [0, 0, BoardMarking.X.value],
            [BoardMarking.X.value, BoardMarking.O.value, 0]
        ])
        _, minimax_move = new_game_with_minimax_player.get_minimax_move_iterative_deepening()
        assert np.all(minimax_move == np.array([1, 0]))

    def test_minimax_makes_blocking_move_south_east_diagonal(self, new_game_with_minimax_player):
        """Test that minimax can win in one move when presented opportunity"""
        new_game_with_minimax_player.starting_player_value = StartingPlayer.PLAYER_O.value
        new_game_with_minimax_player.playing_grid = np.array([
            [BoardMarking.X.value, 0, 0],
            [0, BoardMarking.X.value, BoardMarking.O.value],
            [0, BoardMarking.O.value, 0]
        ])
        _, minimax_move = new_game_with_minimax_player.get_minimax_move_iterative_deepening()
        assert np.all(minimax_move == np.array([2, 2]))
