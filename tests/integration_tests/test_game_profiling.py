"""Integration test for running a profiling simulation - in effect testing most of the backend application."""

# Standard library imports
import pytest

# Local application imports
from automation.game_simulation_base_class import PlayerOptions
from research.game_profiling import GameProfiler


@pytest.fixture(scope="function")
def game_profiler():
    """
    Base fixture for running simulations with. Note that we have False/False for the print/save report,
    because we don't want any of the simulation info here...
    Note also that the RANDOM/RANDOM PlayerOptions is changed for relevant tests.
    """
    profiler = GameProfiler(
        game_rows_m=3, game_cols_n=3, win_length_k=3, number_of_simulations=1,
        player_x_as=PlayerOptions.RANDOM, player_o_as=PlayerOptions.RANDOM,
        print_report=False, save_report=False,
    )
    return profiler


class TestGameProfiler:
    """Class for testing different profiling simulation runs"""
    def test_game_profiler_random_random(self, game_profiler):
        game_profiler.run_profiling_and_profile_processing()

    def test_game_profiler_minimax_random(self, game_profiler):
        game_profiler.player_x_as = PlayerOptions.MINIMAX
        game_profiler.run_profiling_and_profile_processing()
