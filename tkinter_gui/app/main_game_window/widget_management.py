from dataclasses import dataclass
import tkinter as tk
import numpy as np

@dataclass(frozen=False)
class MainWindowWidgetManager:
    """
    Data class that stores all widgets in the main window (across all frames) and therefore allows the widgets within
    the different frames to be tied together in the main window.
    Note only widgets that get updated throughout the game are included here
    """
    playing_grid: np.array = None
    confirmation_button: tk.Button = None
    pos_player_label: tk.Label = None
    neg_player_label: tk.Label = None
    pos_player_win_count_label: tk.Label = None
    neg_player_win_count_label: tk.Label = None
