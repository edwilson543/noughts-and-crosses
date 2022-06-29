"""Module for testing the GameSimulator class"""

# Standard library imports
from datetime import datetime
from pathlib import Path
import pytest

# Third party imports
import numpy as np

# Local application imports
from automation.game_simulation.game_simulation_base_class import GameSimulator
from automation.game_simulation.game_simulation_constants import PlayerOptions, SimulationColumnName
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import StartingPlayer, BoardMarking
from root_directory import ROOT_PATH


@pytest.fixture(scope="module")
def three_three_game_parameters():
    return NoughtsAndCrossesEssentialParameters(
        game_rows_m=3,
        game_cols_n=3,
        win_length_k=3,
        player_x=Player(name="PLAYER_X", marking=BoardMarking.X),
        player_o=Player(name="PLAYER_O", marking=BoardMarking.O),
        starting_player_value=StartingPlayer.PLAYER_X.value)


@pytest.fixture(scope="function")
def three_three_game_simulator(three_three_game_parameters):
    return GameSimulator(
        setup_parameters=three_three_game_parameters,
        number_of_simulations=10,
        player_x_as=PlayerOptions.RANDOM,
        player_o_as=PlayerOptions.RANDOM,
        print_game_outcomes=False,
        save_game_outcome_summary=True,
        save_all_game_data=True,
        output_data_path=ROOT_PATH / "tests" / "test_output_data",  # all gets deleted so doesn't exist
        output_data_file_suffix="_TEST"
    )


class TestGameSimulationBaseClass:
    def test_construct_empty_simulation_dataframe(self, three_three_game_simulator):
        """Tests that the dataframe construction method produces the correct columns for a 3 x 3 game."""
        move = SimulationColumnName.MOVE.name
        board_status = SimulationColumnName.BOARD_STATUS.name
        expected_columns = [SimulationColumnName.STARTING_PLAYER.name, SimulationColumnName.WINNING_PLAYER.name] + \
                           [f"{board_status}_1", f"{board_status}_2", f"{board_status}_3", f"{board_status}_4",
                            f"{board_status}_5",
                            f"{board_status}_6", f"{board_status}_7", f"{board_status}_8", f"{board_status}_9"] + \
                           [f"{move}_1", f"{move}_2", f"{move}_3", f"{move}_4", f"{move}_5", f"{move}_6", f"{move}_7",
                            f"{move}_8", f"{move}_9"]
        actual_columns = three_three_game_simulator._construct_empty_simulation_dataframe().columns
        assert all(expected_columns == actual_columns)

    def test_add_board_status_to_simulation_dataframe(self, three_three_game_simulator):
        """Test that the board status and last move get added to the simulation dataframe in correct place."""
        # Give the game status information to the add_board_status... method
        last_move = np.array([0, 0])
        moves_made = 2
        simulation_number = 10
        three_three_game_simulator.playing_grid = np.array([[1, 1j, 1j], [-1, 1j, 1j], [1j, 1j, 1j]])
        three_three_game_simulator._add_board_status_to_simulation_dataframe(
            last_move=last_move, moves_made=moves_made, simulation_number=simulation_number
        )

        # Check that the game status has been correctly added
        move_str = SimulationColumnName.MOVE.name
        actual_last_move_df = three_three_game_simulator.simulation_dataframe.loc[
            simulation_number, f"{move_str}_{moves_made}"]
        expected_last_move_df = (0, 0)
        assert actual_last_move_df == expected_last_move_df

        board_status_str = SimulationColumnName.BOARD_STATUS.name
        actual_board_status_df = three_three_game_simulator.simulation_dataframe.loc[
            simulation_number, f"{board_status_str}_{moves_made}"]
        expected_board_status_df = ((1, 1j, 1j), (-1, 1j, 1j), (1j, 1j, 1j))
        assert actual_board_status_df == expected_board_status_df

    def test_add_winning_player_to_simulation_dataframe(self, three_three_game_simulator):
        """Test that the correct winning player gets added to the simulation dataframe in correct place."""
        # Give the game status information to the add_winning_player... method
        simulation_number = 10
        three_three_game_simulator.playing_grid = np.array([[1, 1, 1], [-1, -1, 1j], [1j, 1j, 1j]])
        three_three_game_simulator._add_winning_player_to_simulation_dataframe(simulation_number=simulation_number)

        # Check that the game status has been correctly added
        winning_player_column_name = SimulationColumnName.WINNING_PLAYER.name
        actual_winner = three_three_game_simulator.simulation_dataframe.loc[
            simulation_number, winning_player_column_name]
        expected_winner = three_three_game_simulator.player_x.name
        assert actual_winner == expected_winner

    def test_save_simulation_dataframe_to_file(self, three_three_game_simulator):
        """Test that the simulation dataframe is written to file appropriately"""
        three_three_game_simulator._save_simulation_dataframe_to_file()
        date = datetime.now().strftime("%Y_%m_%d")
        file_name = "3_3_3_RANDOM_RANDOM_TEST.csv"
        expected_file_path: Path = three_three_game_simulator.output_data_path / date / file_name
        assert Path.is_file(expected_file_path)
        Path.unlink(expected_file_path)
        Path.rmdir(three_three_game_simulator.output_data_path / date)
        Path.rmdir(three_three_game_simulator.output_data_path)

    def test_save_game_outcome_summary_to_file(self, three_three_game_simulator):
        """Test that the game outcome is written to a text file appropriately"""
        three_three_game_simulator._save_simulation_outcome_summary_to_file()
        date = datetime.now().strftime("%Y_%m_%d")
        file_name = "3_3_3_RANDOM_RANDOM_TEST_SUMMARY.txt"
        expected_file_path: Path = three_three_game_simulator.output_data_path / date / file_name
        assert Path.is_file(expected_file_path)
        Path.unlink(expected_file_path)
        Path.rmdir(three_three_game_simulator.output_data_path / date)
        Path.rmdir(three_three_game_simulator.output_data_path)
