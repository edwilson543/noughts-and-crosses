"""Module to profile all back-end game play code using cProfile"""

# Standard library imports
import cProfile
import pstats
from pathlib import Path

# Local application imports
from root_directory import ROOT_PATH
from automation.game_simulation_base_class import GameSimulator, PlayerOptions
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.game_base_class import Player
from game.constants.game_constants import BoardMarking


####################
# PROFILING Simulation parameters
####################
# Game structure parameters
rows = 3
columns = 3
win_length = 3

# Simulation parameters
number_of_complete_games_to_simulate = 1
player_x_simulated_as = PlayerOptions.MINIMAX
player_o_simulated_as = PlayerOptions.RANDOM

# Reporting parameters
print_report_to_terminal = True
number_of_rows_to_print = 10
save_report_to_file = True  # Note this isn't that useful - dump_stats
saved_report_file_name = "report_profile" + ".log"
####################


class GameProfiler:
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 number_of_simulations: int,
                 player_x_as: PlayerOptions,
                 player_o_as: PlayerOptions,
                 print_report: bool = True,
                 print_entries: int = 10,
                 save_report: bool = False,
                 report_file_path: Path = ROOT_PATH / "research" / "research_data",
                 report_file_name: str = None):
        self.game_parameters = NoughtsAndCrossesEssentialParameters(
            game_rows_m=game_rows_m,
            game_cols_n=game_cols_n,
            win_length_k=win_length_k,
            player_x=Player(name="NOT RELEVANT", marking=BoardMarking.X),
            player_o=Player(name="NOT RELEVANT", marking=BoardMarking.O)
        )
        self.simulation_definition = GameSimulator(
            setup_parameters=self.game_parameters,
            number_of_simulations=number_of_simulations,
            player_x_as=PlayerOptions.MINIMAX,
            player_o_as=PlayerOptions.RANDOM,
            collect_data=False
        )
        self.print_report = print_report
        self.print_entries = print_entries
        self.save_report = save_report
        self.report_file_path = report_file_path
        self.report_file_name = report_file_name

    def run_profiling_and_profile_processing(self) -> None:
        """Method tog generate the profile of the simulated code, manipulate it a bit and print / save it"""
        game_profile = game_profiler.profile_defined_simulation()
        self.print_and_or_save_profile_report(profile=game_profile)

    def profile_defined_simulation(self) -> cProfile.Profile:
        """
        Method to run and profile the simulations defined by the GameSimulator object, and return the profile report.

        Returns: A cProfile.Profile object containing the runtime outcomes of the simulation runs.
        """
        profile = cProfile.Profile()
        profile.enable()
        self.simulation_definition.run_simulations()
        profile.disable()
        return profile

    def print_and_or_save_profile_report(self, profile: cProfile.Profile) -> None:
        """
        Method to print and or save the profile report to file, depending on the instance variables truth.
        Note that both if statements use the pstats print_stats method - this is because the dump_stats method doesn't
        produce human readable files, only files intended to be reloaded. In this context, the purpose of saving the
        profile file is to read it, thus the implementation used.
        """
        if self.print_report:
            report = pstats.Stats(profile)
            report = self.clean_profile_data(report=report)
            print("Report print")
            report.print_stats(self.print_entries)
        if self.save_report:
            file_path = self.report_file_path / self.report_file_name
            with open(file_path, "w") as stream:
                report = pstats.Stats(profile, stream=stream)  # The stream defines where the report gets printed to
                report = self.clean_profile_data(report=report)
                print("Report save")
                report.print_stats()  # Saves the entire log to file

    @staticmethod
    def clean_profile_data(report: pstats.Stats) -> pstats.Stats:
        """Method to clean the pstats.Stats report and return it in the desired format."""
        report.strip_dirs()  # Note this needs to be called before sorting, as it randomises the order
        report.sort_stats(pstats.SortKey.CUMULATIVE)
        return report


if __name__ == "__main__":
    game_profiler = GameProfiler(
        game_rows_m=rows,
        game_cols_n=columns,
        win_length_k=win_length,
        player_x_as=player_x_simulated_as,
        player_o_as=player_o_simulated_as,
        number_of_simulations=number_of_complete_games_to_simulate,
        print_report=print_report_to_terminal,
        print_entries=number_of_rows_to_print,
        save_report=save_report_to_file,
        report_file_name=saved_report_file_name
    )
    game_profiler.run_profiling_and_profile_processing()
