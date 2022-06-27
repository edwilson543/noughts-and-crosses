"""Module used to define the dataclass that manages the widgets in the main_game_window"""

# Standard library imports
from dataclasses import dataclass
import tkinter as tk

# Third party imports
import numpy as np


@dataclass(frozen=False)
class MainWindowWidgetManager:
    """
    Dataclass that stores all widgets in the main main_window (across all frames) and therefore allows the widgets within
    the different frames to be tied together in the main main_window.
    Note only widgets that get updated throughout the game are included here
    """
    # Main main_window
    main_window: tk.Tk = None
    background_frame: tk.Frame = None

    # Playing grid
    playing_grid_frame: tk.Frame = None
    playing_grid: np.array = None
    active_confirmation_button: tk.Button = None
    player_x_confirmation_button: tk.Button = None
    player_o_confirmation_button: tk.Button = None

    # Active game info grid
    game_info_frame: tk.Frame = None
    player_x_label: tk.Label = None
    player_o_label: tk.Label = None

    # Historic game info grid
    historic_info_frame: tk.Frame = None
    player_x_win_count_label: tk.Label = None
    player_o_win_count_label: tk.Label = None
    draw_count_label: tk.Label = None
