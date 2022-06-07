from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from enum import Enum, auto
from typing import List
import numpy as np


class PlayerOptions(Enum):
    """Enumeration of the different player options the simulated players can be."""
    MINIMAX = auto()
    RANDOM = auto()


class GameSimulator(NoughtsAndCrossesMinimax):
    """
    Class to run simulations of the noughts and crosses game, for profiling and data collection.

    Instance attributes:
    __________
    # TODO
    """
    def __init__(self,
                 number_of_simulations: int,
                 player_x_as: PlayerOptions,
                 player_o_as: PlayerOptions,
                 collect_data: bool,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0):
        super().__init__(setup_parameters, draw_count)
        self.number_of_simulations = number_of_simulations
        self.player_x_as = player_x_as
        self.player_o_as = player_o_as
        self.collect_data = collect_data

    def run_simulations(self):
        """Method to call to run the simulations of the game play"""

        # Potentially some setup methods
        for simulation_number in range(0, self.number_of_simulations):
            self.set_starting_player(starting_player_value=StartingPlayer.RANDOM.value)
            game_depth = 0
            while True:
                if self.get_player_turn() == BoardMarking.X.value:
                    marking_index = self._get_player_x_move()
                else:
                    marking_index = self._get_player_o_move()
                self.mark_board(marking_index=marking_index)
                game_depth += 1
                # Add the game status to iloc[simulation_number, turn_number] - possibly its own method
                if self.win_check_and_location_search(last_played_index=marking_index, get_win_location=False):
                    # Add the game outcome to data
                    self.reset_game_board()
                    break
                elif self.check_for_draw():
                    # Add the game outcome to data
                    self.reset_game_board()
                    break

    # Methods used to generate the player moves when running the simulations
    def _get_player_x_move(self) -> np.ndarray:
        """Method to get the moved played by player x on their turn"""
        if self.player_x_as == PlayerOptions.MINIMAX:
            _, move = self.get_minimax_move()
            return move
        elif self.player_x_as == PlayerOptions.RANDOM:
            return self._get_random_move()
        else:
            raise ValueError(f"player_x_as simulation player's moves are not defined."
                             f"self.player_x_as: {self.player_x_as}")

    def _get_player_o_move(self) -> np.array:
        """Method to get the moved played by player o on their turn"""
        if self.player_x_as == PlayerOptions.MINIMAX:
            _, move = self.get_minimax_move()
            return move
        elif self.player_x_as == PlayerOptions.RANDOM:
            return self._get_random_move()
        else:
            raise ValueError(f"player_o_as simulation player's moves are not defined."
                             f"self.player_x_as: {self.player_x_as}")

    def _get_random_move(self):
        """
        Method to generate a random move on the playing grid.
        Note that the _get_available_cell_indices method already includes a random shuffle, so we can just index of
        the first element in this list.
        """
        random_options: List[np.ndarray] = self._get_available_cell_indices(playing_grid=self.playing_grid)
        return random_options[0]


