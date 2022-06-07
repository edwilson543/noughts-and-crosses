"""Module to profile all back-end game play code using cProfile"""

# Standard library imports
import cProfile
import pstats

# Local application imports
from automation.game_simulation_base_class import GameSimulator, PlayerOptions
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.game_base_class import Player
from game.constants.game_constants import BoardMarking

##########
# PROFILING Simulation parameters
##########
game_rows_m = 3
game_cols_n = 3
win_length_k = 3

number_of_simulations = 2

player_x_as = PlayerOptions.MINIMAX
player_o_as = PlayerOptions.RANDOM

print_report = True
save_report = True  # TODO
save_report_file_name = "my_file"  # TODO
##########


def profile_defined_simulation(run_definition: GameSimulator) -> cProfile.Profile:
    """
    Function to run and profile the simulations defined by the GameSimulator object, and return the profile report.

    Parameters: run_definition - the fully defined simulation object we will be running the simulation for
    Returns: A cProfile.Profile object containing the runtime outcomes of the simulation runs.
    """
    profile = cProfile.Profile()
    profile.enable()
    run_definition.run_simulations()
    profile.disable()
    return profile


def clean_profile_data(profile: cProfile.Profile) -> pstats.Stats:
    """Function to clean the profile and return it in the desired format, as a pstats.Stats object"""
    report = pstats.Stats(profile)
    report.strip_dirs()  # Note this needs to be called before sorting, as randomises the order
    report.sort_stats(pstats.SortKey.CUMULATIVE)
    return report


if __name__ == "__main__":
    game_parameters = NoughtsAndCrossesEssentialParameters(
        game_rows_m=game_rows_m,
        game_cols_n=game_cols_n,
        win_length_k=win_length_k,
        player_x=Player(name="NOT RELEVANT", marking=BoardMarking.X),
        player_o=Player(name="NOT RELEVANT", marking=BoardMarking.O)
    )

    run = GameSimulator(
        setup_parameters=game_parameters,
        number_of_simulations=2,
        player_x_as=PlayerOptions.MINIMAX,
        player_o_as=PlayerOptions.RANDOM,
        collect_data=False
    )

    game_profile = profile_defined_simulation(run_definition=run)
    simulation_report = clean_profile_data(profile=game_profile)

    if print_report:
        simulation_report.print_stats(10)
