"""Module to profile all back-end game play code using cProfile"""

# Standard library imports
import cProfile
import pstats

# Local application imports
from automation.game_simulation_base_class import GameSimulator, PlayerOptions
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.game_base_class import Player
from game.constants.game_constants import BoardMarking

if __name__ == "__main__":
    game_parameters = NoughtsAndCrossesEssentialParameters(
        game_rows_m=3,
        game_cols_n=3,
        win_length_k=3,
        player_x=Player(name="Minimax player", marking=BoardMarking.X),
        player_o=Player(name="Random player", marking=BoardMarking.O)
    )

    simulation_run = GameSimulator(
        setup_parameters=game_parameters,
        number_of_simulations=2,
        player_x_as=PlayerOptions.MINIMAX,
        player_o_as=PlayerOptions.RANDOM,
        collect_data=False
    )

    game_profile = cProfile.Profile()
    game_profile.enable()
    simulation_run.run_simulations()
    game_profile.disable()

    simulation_report = pstats.Stats(game_profile)
    simulation_report.strip_dirs()  # Note this needs to be called before sorting, as randomises the order
    simulation_report.sort_stats(pstats.SortKey.CUMULATIVE)
    simulation_report.print_stats(10)
