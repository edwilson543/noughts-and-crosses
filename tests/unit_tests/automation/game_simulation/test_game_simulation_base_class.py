# Standard library imports
import pytest

# Third party imports
import numpy as np

# Local application imports
from automation.game_simulation.game_simulation_base_class import GameSimulator
from automation.game_simulation.game_simulation_constants import PlayerOptions, SimulationColumnName
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import StartingPlayer, BoardMarking


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
        collect_data=True,
    )


class TestGameSimulationBaseClass:
    def test_construct_empty_simulation_dataframe(self, three_three_game_simulator):
        """Tests that the dataframe construction method produces the correct columns for a 3 x 3 game."""
        move = SimulationColumnName.MOVE.name
        board_status = SimulationColumnName.BOARD_STATUS.name
        expected_columns = [SimulationColumnName.STARTING_PLAYER.name, SimulationColumnName.WINNING_PLAYER.name] + \
            [f"{board_status}_1", f"{board_status}_2", f"{board_status}_3", f"{board_status}_4", f"{board_status}_5",
             f"{board_status}_6", f"{board_status}_7", f"{board_status}_8", f"{board_status}_9"] + \
        [f"{move}_1", f"{move}_2", f"{move}_3", f"{move}_4", f"{move}_5", f"{move}_6", f"{move}_7", f"{move}_8",
         f"{move}_9"]
        actual_columns = three_three_game_simulator._construct_empty_simulation_dataframe().columns
        assert all(expected_columns == actual_columns)

    # TODO - pending decision on what the best way to store the board string is
    # def test_encode_string_to_board(self, three_three_game_simulator):
    #     """Test that the correct string representation of the board is produced"""
    #     three_three_game_simulator.playing_grid = np.array([
    #         [BoardMarking.X.value, BoardMarking.O.value, 0],
    #         [0, 0, 0],
    #         [0, 0, 0],
    #         ])
    #     expected_string = "[['X' 'O' '-']\n['-' '-' '-']\n['-' '-' '-']]"
    #     actual_string = three_three_game_simulator._encode_board_as_string()
    #     assert expected_string == actual_string

