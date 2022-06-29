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
from utils import np_array_to_tuple


class GameSimulator(NoughtsAndCrossesMinimax):
    """
    Class to DEFINE simulation parameters of the noughts and crosses game.
    These can be used for profiling, data collection, etc.

    Instance attributes:
    __________
    setup_parameters: The parameters used to define the game of noughts and crosses that are being played
    number_of_simulations: The number of games that will be simulated to completion between the two players
    player_x_as/player_o_as: The automatic players X and O will be simulated as
    print_game_outcomes: Whether or not how many games each player wins gets printed to the terminal
    collect_data: True/False depending on whether we want to store the simulated games
    collect_data_path: The path where the collected data will be saved (plus an additional /date)
    collect_data_file_suffix: The suffix to the file where the data is being saved (plus an m_n_k prefix)
    simulation_dataframe: The dataframe used to store the moves, board status and outcomes of individual games
    """

    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 number_of_simulations: int,
                 player_x_as: PlayerOptions,
                 player_o_as: PlayerOptions,
                 print_game_outcomes: bool,
                 save_game_outcome_summary: bool,
                 save_all_game_data: bool,
                 output_data_path: Path = ROOT_PATH / "research" / "game_simulation_data",
                 output_data_file_suffix: str = None):
        super().__init__(setup_parameters)
        self.number_of_simulations = number_of_simulations
        self.player_x_as = player_x_as
        self.player_o_as = player_o_as
        self.print_game_outcomes = print_game_outcomes
        self.save_game_outcome_summary = save_game_outcome_summary
        self.save_all_game_data = save_all_game_data
        self.collect_data = print_game_outcomes or save_game_outcome_summary or save_all_game_data
        self.output_data_path = output_data_path
        self.output_data_file_suffix = output_data_file_suffix
        self.simulation_dataframe: pd.DataFrame = self._construct_empty_simulation_dataframe()

    def run_simulations(self):
        """Method that gets called to run the simulations of the game play"""

        # Potentially some setup methods
        for simulation_number in range(0, self.number_of_simulations):
            # Determine a random starting player and store this
            self.set_starting_player(starting_player_value=StartingPlayer.RANDOM.value)
            if self.collect_data:
                self.simulation_dataframe.loc[
                    simulation_number, SimulationColumnName.STARTING_PLAYER.name] = StartingPlayer(
                    self.starting_player_value).name

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
                        last_move=marking_index, moves_made=moves_made, simulation_number=simulation_number)

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

        if self.save_all_game_data:
            self._save_simulation_dataframe_to_file()
        if self.save_game_outcome_summary:
            self._save_simulation_outcome_summary_to_file()
        if self.print_game_outcomes:
            self._print_simulation_outcome_to_terminal()

    # Methods used to generate the player moves when running the simulations
    def _get_player_x_move(self) -> np.ndarray:
        """Method to get the moved played by player x on their turn"""
        if self.player_x_as == PlayerOptions.MINIMAX:
            _, move = self.get_minimax_move_iterative_deepening()
            return move
        elif self.player_x_as == PlayerOptions.RANDOM:
            return self._get_random_move()
        else:
            raise ValueError(f"player_x_as simulation player's moves are not defined."
                             f"self.player_x_as: {self.player_x_as}")

    def _get_player_o_move(self) -> np.ndarray:
        """Method to get the moved played by player o on their turn"""
        if self.player_o_as == PlayerOptions.MINIMAX:
            _, move = self.get_minimax_move_iterative_deepening()
            return move
        elif self.player_o_as == PlayerOptions.RANDOM:
            return self._get_random_move()
        else:
            raise ValueError(f"player_o_as simulation player's moves are not defined."
                             f"self.player_o_as: {self.player_o_as}")

    def _get_random_move(self) -> np.ndarray:
        """
        Method to generate a random move on the playing grid.
        Note that the _get_available_cell_indices method already includes a random shuffle, so we can just index out
        the first element in this list.
        Note also that despite it returning a sliced list, because it is randomly sliced, this does not matter
        """
        random_options: List[np.ndarray] = self._get_available_cell_indices(
            playing_grid=self.playing_grid, search_depth=0)
        return random_options[0]

    # Methods relating to creating, populating and saving the data structure for collecting simulation data
    def _construct_empty_simulation_dataframe(self) -> pd.DataFrame:
        """Method to initialise an empty pandas DataFrame in the relevant structure for collecting game data."""
        if self.collect_data:
            possible_moves = self.game_rows_m * self.game_cols_n
            columns = [SimulationColumnName.STARTING_PLAYER.name, SimulationColumnName.WINNING_PLAYER.name] + \
                      [f"{SimulationColumnName.BOARD_STATUS.name}_{move_number + 1}" for move_number in
                       range(0, possible_moves)] + \
                      [f"{SimulationColumnName.MOVE.name}_{move_number + 1}" for move_number in
                       range(0, possible_moves)]
            index = pd.RangeIndex(0, self.number_of_simulations)
            simulation_dataframe = pd.DataFrame(columns=columns, index=index, dtype=str)
            return simulation_dataframe

    def _add_board_status_to_simulation_dataframe(self, last_move: np.ndarray, moves_made: int,
                                                  simulation_number: int) -> None:
        """
        Method to add the current status and previous move of the board to the simulation dataframe,
        in the relevant row and column.
        """
        board_status_col_index = f"{SimulationColumnName.BOARD_STATUS.name}_{moves_made}"
        self.simulation_dataframe.loc[simulation_number, board_status_col_index] = np_array_to_tuple(self.playing_grid)

        last_move_col_index = f"{SimulationColumnName.MOVE.name}_{moves_made}"
        self.simulation_dataframe.loc[simulation_number, last_move_col_index] = np_array_to_tuple(last_move)

    def _add_winning_player_to_simulation_dataframe(self, simulation_number: int) -> None:
        """Method to add the winning player to the dataframe, in the case that we know there is a winner."""
        last_played_value = - self.get_player_turn()
        if BoardMarking(last_played_value) == BoardMarking.X:
            self.simulation_dataframe.loc[
                simulation_number, SimulationColumnName.WINNING_PLAYER.name] = self.player_x.name
        else:
            self.simulation_dataframe.loc[
                simulation_number, SimulationColumnName.WINNING_PLAYER.name] = self.player_o.name

    def _save_simulation_dataframe_to_file(self) -> None:
        """Method to save the simulation file in the given path."""
        date_directory_name = datetime.now().strftime("%Y_%m_%d")
        file_path: Path = self.output_data_path / date_directory_name
        if not file_path.is_dir():
            file_path.mkdir(parents=True)

        file_name = self.get_output_file_prefix() + self.output_data_file_suffix + ".csv"
        self.simulation_dataframe.to_csv(file_path / file_name, index=False, na_rep="GAME_WON")

    def _save_simulation_outcome_summary_to_file(self) -> None:
        """
        Method to save the simulation outcomes to file in the given path. This will be in the same place as the
        save_simulation_dataframe_to_file, but with a summary_prefix
        """
        date_directory_name = datetime.now().strftime("%Y_%m_%d")
        file_path: Path = self.output_data_path / date_directory_name
        if not file_path.is_dir():
            file_path.mkdir(parents=True)

        file_name = self.get_output_file_prefix() + self.output_data_file_suffix + "_SUMMARY" + ".txt"
        full_file_path = file_path / file_name
        text = self._get_simulation_outcome_summary_text()
        with open(full_file_path, "w") as write_file:
            write_file.write(text)

    def _print_simulation_outcome_to_terminal(self) -> None:
        """Method to print a summary of who won how many games to the terminal."""
        text = self._get_simulation_outcome_summary_text()
        print(text)

    def _get_simulation_outcome_summary_text(self) -> str:
        """
        Method producing a summary of the simulated game and simulation parameters, including a record of the
        aggregated outcomes of all the games (i.e. either player's win counts).
        """
        overview_text = self.get_string_detailing_simulation_parameters()
        win_counts = self.simulation_dataframe[SimulationColumnName.WINNING_PLAYER.name].value_counts(ascending=False)
        win_counts_text = f"Summary of games won by each player during the simulations:\n{win_counts}"
        full_text = overview_text + "\n" + win_counts_text
        return full_text

    # Methods producing strings detailing metadata related to simulation
    def get_output_file_prefix(self) -> str:
        """Method to create a string of the form: 3_3_3_MINIMAX_RANDOM as a prefix for saved data files"""
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
