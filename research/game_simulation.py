"""
Module to run simulations of the game.
Data can be saved for later analysis/ use in a transposition table, or just a quick print to summarise the game
outcomes can be chosen.
Note that this is different to the game_profiling in that the purpose of this module is to collect the data/ assess
game outcomes, not to time different components of the code.
"""

# Local application imports
from automation.game_simulation.game_simulation_base_class import GameSimulator
from automation.game_simulation.game_simulation_constants import PlayerOptions
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking
from root_directory import ROOT_PATH

####################
# GAME SIMULATION parameters
####################
# Game structure parameters
rows = 3
columns = 3
win_length = 3

# Simulation parameters
number_of_complete_games_to_simulate = 3
player_x_simulated_as = PlayerOptions.MINIMAX
player_o_simulated_as = PlayerOptions.RANDOM

# Reporting parameters
print_game_outcomes = True
save_game_outcome_summary = True
save_all_game_data = False
data_file_suffix = "_my_simulation"  # Note 'suffix' because simulation metadata auto included. Extension too.
data_file_path = ROOT_PATH / "research" / "game_simulation_data"
####################

if __name__ == "__main__":
    setup_parameters = NoughtsAndCrossesEssentialParameters(
        game_rows_m=rows,
        game_cols_n=columns,
        win_length_k=win_length,
        player_x=Player(name="PLAYER_X", marking=BoardMarking.X),
        player_o=Player(name="PLAYER_O", marking=BoardMarking.O)
    )
    game_simulator = GameSimulator(
        setup_parameters=setup_parameters,
        number_of_simulations=number_of_complete_games_to_simulate,
        player_x_as=player_x_simulated_as,
        player_o_as=player_o_simulated_as,
        print_game_outcomes=print_game_outcomes,
        save_game_outcome_summary=save_game_outcome_summary,
        save_all_game_data=save_all_game_data,
        output_data_path=data_file_path,
        output_data_file_suffix=data_file_suffix,
    )
    game_simulator.run_simulations()
