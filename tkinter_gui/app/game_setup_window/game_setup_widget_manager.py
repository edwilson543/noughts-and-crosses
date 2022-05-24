from dataclasses import dataclass
from tkinter import ttk


@dataclass(frozen=False)
class GameSetupWidgets:
    # Game parameters
    game_parameters_frame: ttk.Frame = None
    game_rows_scale: ttk.Scale = None
    game_rows_label: ttk.Label = None
    game_cols_scale: ttk.Scale = None
    game_cols_label: ttk.Label = None
    win_length_scale: ttk.Scale = None
    win_length_label: ttk.Label = None

    # Player info
    player_info_frame: ttk.Frame = None
    pos_player_entry: ttk.Entry = None
    pos_player_prompt_label: ttk.Label = None
    pos_player_starts_radio: ttk.Radiobutton = None
    neg_player_entry: ttk.Entry = None
    neg_player_prompt_label: ttk.Label = None
    neg_player_starts_radio: ttk.Radiobutton = None
    random_player_starts_radio: ttk.Radiobutton = None

    # Universal
    confirmation_button: ttk.Button = None
