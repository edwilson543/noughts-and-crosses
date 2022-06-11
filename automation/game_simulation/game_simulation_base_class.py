"""Module for defining how simulations of noughts and crosses can be run."""

# Standard library imports
from datetime import datetime
from pathlib import Path
from typing import List

# Third party imports
import numpy as np
import pandas as pd

# Local application imports
from automation.game_simulation.game_simulation_constants import SimulationColumnName, PlayerOptions
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import StartingPlayer, BoardMarking
from root_directory import ROOT_PATH


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
                 collected_data_path: Path = ROOT_PATH / "research" / "game_simulation_data",
                 collected_data_file_suffix: str = None):
        super().__init__(setup_parameters)
        self.number_of_simulations = number_of_simulations
        self.player_x_as = player_x_as
        self.player_o_as = player_o_as
        self.collect_data = collect_data
        self.collected_data_path = collected_data_path
        self.collected_data_file_suffix = collected_data_file_suffix
        self.simulation_dataframe: pd.DataFrame = self._construct_empty_simulation_dataframe()

    def run_simulations(self):
        """Method to call to run the simulations of the game play"""

        # Potentially some setup methods
        for simulation_number in range(0, self.number_of_simulations):
            # Determine a random starting player and store this
            self.set_starting_player(starting_player_value=StartingPlayer.RANDOM.value)
            if self.collect_data:
                self.simulation_dataframe.loc[
                    simulation_number, SimulationColumnName.STARTING_PLAYER.name] = self.starting_player_value

            moves_made = 0
            while True:  # player o and player x successively makes moves until the game is won or drawn
                if self.get_player_turn() == BoardMarking.X.value:
                    marking_index = self._get_player_x_move()
                else:
                    marking_index = self._get_player_o_move()
                self.mark_board(marking_index=marking_index)
                moves_made += 1

                if self.collect_data:
                    self._add_board_status_to_simulation_dataframe(
                        moves_made=moves_made, simulation_number=simulation_number)

                # If there has been a draw or a win, store this information and simulated the next game
                win, _ = self.win_check_and_location_search(last_played_index=marking_index, get_win_location=False)
                if win:
                    if self.collect_data:
                        self._add_winning_player_to_simulation_dataframe(simulation_number=simulation_number)
                    self.reset_game_board()
                    break
                elif self.check_for_draw():
                    if self.collect_data:
                        self.simulation_dataframe.loc[
                            simulation_number, SimulationColumnName.WINNING_PLAYER.name] = "DRAW"
                    self.reset_game_board()
                    break
        self._save_simulation_dataframe_to_file()

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

    # Methods relating to creating, populating and saving the data structure for collecting simulation data
    def _construct_empty_simulation_dataframe(self) -> pd.DataFrame:
        """Method to initialise an empty pandas DataFrame in the relevant structure for collecting game data."""
        if self.collect_data:
            possible_moves = self.game_rows_m * self.game_cols_n
            columns = [SimulationColumnName.STARTING_PLAYER.name, SimulationColumnName.WINNING_PLAYER.name] + \
                      [f"{SimulationColumnName.MOVE.name}_{move_number + 1}" for move_number in
                       range(0, possible_moves)]
            index = pd.RangeIndex(0, self.number_of_simulations)
            simulation_dataframe = pd.DataFrame(columns=columns, index=index, dtype=str)
            return simulation_dataframe

    def _add_board_status_to_simulation_dataframe(self, moves_made: int, simulation_number: int) -> None:
        """Method to add the current status of the board to the simulation dataframe, in the correct place"""
        col_index = f"{SimulationColumnName.MOVE.name}_{moves_made}"
        self.simulation_dataframe.loc[simulation_number, col_index] = self._encode_board_as_string()

    def _add_winning_player_to_simulation_dataframe(self, simulation_number: int) -> None:
        """Method to add the winning player to the dataframe, in the case that we no there is a winner."""
        last_played_value = self.get_player_turn()
        if BoardMarking(last_played_value) == BoardMarking.X:
            self.simulation_dataframe.loc[
                simulation_number, SimulationColumnName.WINNING_PLAYER.name] = BoardMarking.X.name
        else:
            self.simulation_dataframe.loc[
                simulation_number, SimulationColumnName.WINNING_PLAYER.name] = BoardMarking.O.name

    def _save_simulation_dataframe_to_file(self):
        """Method to save the simulation file in the given path."""
        date_directory_name = datetime.now().strftime("%Y_%m_%d")
        file_path: Path = self.collected_data_path / date_directory_name
        if not file_path.is_dir():
            file_path.mkdir(parents=True)

        file_name = self.get_output_file_prefix() + self.collected_data_file_suffix + ".csv"
        self.simulation_dataframe.to_csv(file_path / file_name)

    def _encode_board_as_string(self) -> str:
        """Method that converts the numpy array board into a human readable string"""
        element_wise_int_to_str_func = np.vectorize(lambda mark: BoardMarking(mark).name if mark != 0 else "-")
        np_array_of_strings = element_wise_int_to_str_func(self.playing_grid)
        array_string = np.array2string(np_array_of_strings)
        return array_string

    # Methods producing strings detailing metadata related to simulation
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
