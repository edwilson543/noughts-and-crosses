"""
Module to run simulations where the aim is to profile all back-end game play code using cProfile.
Note this is separated from the simulation use case to collect data for 2 reasons:
1) Extra set-up is needed with cProfile and report manipulation versus just running the collections
2) Saving the data is slow and not that interesting from a speeding-up point of view, the purpose of the profiling is
to look at making the search and minimax more efficient.
"""

# Standard library imports
import cProfile
import pstats
from pathlib import Path
from datetime import datetime

# Local application imports
from root_directory import ROOT_PATH
from automation.game_simulation.game_simulation_base_class import GameSimulator
from automation.game_simulation.game_simulation_constants import PlayerOptions
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
number_of_complete_games_to_simulate = 10
player_x_simulated_as = PlayerOptions.MINIMAX
player_o_simulated_as = PlayerOptions.RANDOM

# Reporting parameters
print_report_to_terminal = True
number_of_rows_to_print = 10
save_report_to_file = True
saved_report_file_suffix = "_iterative_deepening_scoring_func"  # Note 'suffix' because simulation metadata auto included. Extension too.
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
                 report_file_path: Path = ROOT_PATH / "research" / "profiling_data",
                 report_file_name: str = None,
                 report_file_suffix: str = ".log"):
        self.game_parameters = NoughtsAndCrossesEssentialParameters(
            game_rows_m=game_rows_m,
            game_cols_n=game_cols_n,
            win_length_k=win_length_k,
            player_x=Player(name="NOT_RELEVANT", marking=BoardMarking.X),
            player_o=Player(name="NOT_RELEVANT", marking=BoardMarking.O)
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
        self.report_file_suffix = report_file_name
        self.report_file_extension = report_file_suffix

    def run_profiling_and_profile_processing(self) -> None:
        """Method to generate the profile of the simulated code, manipulate it a bit and print / save it"""
        game_profile = self.profile_defined_simulation()
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
        """
        if self.print_report:
            self._print_report_to_terminal(profile=profile)
        if self.save_report:
            self._save_report_to_file(profile=profile)

    def _print_report_to_terminal(self, profile: cProfile.Profile) -> None:
        """Method to print the profiling report directly to the terminal"""
        report = pstats.Stats(profile)
        report = self._clean_profile_data(report=report)
        print(self.simulation_definition.get_string_detailing_simulation_parameters())
        report.print_stats(self.print_entries)

    def _save_report_to_file(self, profile: cProfile.Profile) -> None:
        """
        Method to save the profiling report to file.
        Note that the pstats the dump_stats method doesn't produce human readable files, only files intended to be
        reloaded. In this context, the purpose of saving the profile file is to read it, thus the implementation used,
        rather than dump_stats
        """
        datetime_label = datetime.now().strftime("%Y_%m_%d")
        temporary_file_path = self.report_file_path / datetime_label / "temporary_file.log"
        saved_file_path = self.report_file_path / datetime_label / self._get_full_report_file_name()
        # Note that the temporary/saved file is so that we can add some simulation metadata to the start of the file

        if not Path.is_dir(self.report_file_path / datetime_label):
            Path.mkdir(self.report_file_path / datetime_label, parents=True)
        with open(temporary_file_path, "w") as stream:
            report = pstats.Stats(profile, stream=stream)  # The stream defines where the report gets printed to
            report = self._clean_profile_data(report=report)
            report.print_stats()  # Saves the entire log to file
        with open(temporary_file_path, "r") as temporary_file, open(saved_file_path, "w") as saved_file:
            saved_file.write(self.simulation_definition.get_string_detailing_simulation_parameters())
            old_content = temporary_file.readlines()
            saved_file.writelines(old_content)
        temporary_file_path.unlink()  # Delete the temporary file

    @staticmethod
    def _clean_profile_data(report: pstats.Stats) -> pstats.Stats:
        """Method to clean the pstats.Stats report and return it in the desired format."""
        report.strip_dirs()  # Note this needs to be called before sorting, as it randomises the order
        report.sort_stats(pstats.SortKey.CUMULATIVE)
        return report

    def _get_full_report_file_name(self) -> str:
        """Method to get the full name of the file to be used for the file."""
        prefix = self.simulation_definition.get_output_file_prefix()
        return prefix + self.report_file_suffix + self.report_file_extension


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
        report_file_name=saved_report_file_suffix
    )
    game_profiler.run_profiling_and_profile_processing()
