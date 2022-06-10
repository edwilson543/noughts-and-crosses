"""Module for defining how simulations of noughts and crosses can be run."""

# Standard library imports
from typing import List
from pathlib import Path

# Third party imports
import numpy as np
import pandas as pd

# Local application imports
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from automation.game_simulation.game_simulation_constants import SimulationColumnName, PlayerOptions


class GameSimulator(NoughtsAndCrossesMinimax):
    """
    Class to DEFINE simulation parameters of the noughts and crosses game.
    These can be used for profiling, data collection, etc.

    Instance attributes:
    __________
    number_of_simulations: The number of games that will be simulated to completion between the two players
    player_x_as/player_o_as: The automatic players X and O will be simulated as
    collect_data: True/False depending on whether we want to store the simulated games
    setup_parameters: The parameters of the game we are simulating
    draw_count: The count of the number of draws for the game we are simulating
    """

    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 number_of_simulations: int,
                 player_x_as: PlayerOptions,
                 player_o_as: PlayerOptions,
                 collect_data: bool,
                 collected_data_path: Path = None,
                 collected_data_file_suffix: Path = None):
        super().__init__(setup_parameters)
        self.number_of_simulations = number_of_simulations
        self.player_x_as = player_x_as
        self.player_o_as = player_o_as
        self.collect_data = collect_data
        self.simulation_data = self._construct_empty_simulation_dataframe()

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
        Method to generate arr random move on the playing grid.
        Note that the _get_available_cell_indices method already includes arr random shuffle, so we can just index of
        the first element in this list.
        """
        random_options: List[np.ndarray] = self._get_available_cell_indices(playing_grid=self.playing_grid)
        return random_options[0]

    # Methods relating to data structure for the collected simulation data
    def _construct_empty_simulation_dataframe(self) -> pd.DataFrame:
        """Method to initialise an empty pandas DataFrame in the relevant structure for collecting game data."""
        if self.collect_data:
            possible_moves = self.game_rows_m * self.game_cols_n
            columns = [SimulationColumnName.STARTING_PLAYER.name, SimulationColumnName.WINNING_PLAYER.name] + \
                [f"{SimulationColumnName.MOVE.name}_{move_number+1}" for move_number in range(0, possible_moves)]
            index = pd.RangeIndex(0, self.number_of_simulations)
            simulation_dataframe = pd.DataFrame(columns=columns, index=index, dtype=str)
            return simulation_dataframe

    def _encode_board_as_string(self) -> str:
        """Method that converts the numpy array board into a human readable string"""
        element_wise_int_to_str_func = np.vectorize(lambda mark: BoardMarking(mark).name if mark != 0 else "-")
        np_array_of_strings = element_wise_int_to_str_func(self.playing_grid)
        array_string = np.array2string(np_array_of_strings)
        return array_string

    # Methods relating to output metadata
    def get_output_file_prefix(self) -> str:
        """Method to create a string of the form: 3_3_3_MINIMAX_RANDOM as a prefix for data files"""
        text = f"{self.game_rows_m}_{self.game_cols_n}_{self.win_length_k}_{self.player_x_as.name}_" \
               f"{self.player_o_as.name}"
        return text

    def get_string_detailing_simulation_parameters(self) -> str:
        """Method to generate a string representation of the simulation run that we are profiling"""
        text = f"########## Simulation parameters ##########\n\n" \
               f"(m, n, k) = ({self.game_rows_m}, {self.game_cols_n}, {self.win_length_k})\n" \
               f"Number of finished games simulated: {self.number_of_simulations}\n" \
               f"Player X was simulated as: {self.player_x_as.name}\n" \
               f"Player O was simulated as: {self.player_o_as.name}\n\n" \
               f"###########################################\n\n"
        return text
