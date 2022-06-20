"""
Module to run simulations where the purpose is to save the simulation data.
The purpose of saving such data is to, for example, create a play book of different moves that algorithms can look up
from to get the optimum first 2/3 moves while there is little information to go off in the actual game.
Another purpose is to review how effective minimax is at different game parameters.

All data is saved in CSV format, with one row per simulated game - a good alternative to look into could be to save game
trees as nested JSON dicts, where the key at each nest is the state of the board, and the value is all boards
branching from that state. The final values could then be the win count along a given branch.
"""

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
rows = 10
columns = 10
win_length = 3

# Simulation parameters
number_of_complete_games_to_simulate = 10
player_x_simulated_as = PlayerOptions.MINIMAX
player_o_simulated_as = PlayerOptions.RANDOM

# Reporting parameters
print_game_outcomes = True
data_file_suffix = "_sim_str"  # Note 'suffix' because simulation metadata auto included. Extension too.
data_file_path = ROOT_PATH / "research" / "game_simulation_data"
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
        print_game_outcomes=print_game_outcomes,
        collect_data=True,
        collected_data_path=data_file_path,
        collected_data_file_suffix=data_file_suffix,
    )
    game_simulator.run_simulations()
