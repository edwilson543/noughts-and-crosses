"""Module to run simulations where the purpose is to save the simulation data."""

# Local application imports
from automation.game_simulation.game_simulation_base_class import GameSimulator
from automation.game_simulation.game_simulation_constants import PlayerOptions
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking
from root_directory import ROOT_PATH

####################
# DATA COLLECTION Simulation parameters
####################
# Game structure parameters
rows = 3
columns = 3
win_length = 3

# Simulation parameters
number_of_complete_games_to_simulate = 100
player_x_simulated_as = PlayerOptions.RANDOM
player_o_simulated_as = PlayerOptions.RANDOM

# Reporting parameters
data_file_path = ROOT_PATH / "research" / "game_simulation_data"
data_file_suffix = "_standard_sim"  # Note 'suffix' because simulation metadata auto included. Extension too.
####################

if __name__ == "__main__":
    setup_parameters = NoughtsAndCrossesEssentialParameters(
        game_rows_m=rows,
        game_cols_n=columns,
        win_length_k=win_length,
        player_x=Player(name="NOT_RELEVANT", marking=BoardMarking.X),
        player_o=Player(name="NOT_RELEVANT", marking=BoardMarking.O)
    )
    game_simulator = GameSimulator(
        setup_parameters=setup_parameters,
        number_of_simulations=number_of_complete_games_to_simulate,
        player_x_as=player_x_simulated_as,
        player_o_as=player_o_simulated_as,
        collect_data=True,
        collected_data_path=data_file_path,
        collected_data_file_suffix=data_file_suffix
    )
    game_simulator.run_simulations()
