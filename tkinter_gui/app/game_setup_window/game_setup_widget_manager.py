from dataclasses import dataclass
from tkinter import ttk
import tkinter as tk

@dataclass(frozen=False)
class GameSetupWidgets:
    # Setup window
    setup_window: tk.Tk = None

    # Game parameters
    game_parameters_frame: ttk.Frame = None
    game_rows_scale: tk.Scale = None
    game_rows_label: ttk.Label = None
    game_cols_scale: tk.Scale = None
    game_cols_label: ttk.Label = None
    win_length_scale: tk.Scale = None
    win_length_label: ttk.Label = None

    # Player info
    player_info_frame: tk.Frame = None
    pos_player_entry: tk.Entry = None
    pos_player_prompt_label: tk.Label = None
    neg_player_entry: tk.Entry = None
    neg_player_prompt_label: tk.Label = None
    pos_player_starts_radio: ttk.Radiobutton = None
    neg_player_starts_radio: ttk.Radiobutton = None
    random_player_starts_radio: ttk.Radiobutton = None

    # Universal
    confirmation_button: ttk.Button = None
