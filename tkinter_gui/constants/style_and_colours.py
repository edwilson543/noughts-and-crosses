from enum import Enum
import tkinter as tk


class Colour(Enum):
    window = "black"
    background = "black"

    # Inside the frames on the mian window
    game_background = "#d1c7c7"
    game_buttons_background = "#b2d1f7"
    game_status_background = "#78f599"

    # Inside the playing grid
    available_cell = "#fffad6"
    occupied_cell_o = "#dedede"
    occupied_cell_x = "#8c8b8b"
    unconfirmed_cell = "#ffabfc"
    unconfirmed_cell_font = "black"

    # Inside the game info frame
    info_panels_font = "black"
    players_turn_label = "#8bb2f0"
    players_turn_font = "black"

    # Inside the historic game info frame
    game_win_count_label = "#013d0c"
    game_win_count_font = "white"
    player_win_count_labels = "#013d0c"
    player_win_count_font = "white"


class Font(Enum):
    xo_font = "Times New Roman"
    default_font = "Didot"


class Relief(Enum):
    # Playing grid
    available_cell = tk.RAISED
    unconfirmed_cell = tk.RAISED
    occupied_cell = tk.SUNKEN

    # Active info grid
    players_turn = tk.SUNKEN
    active_player_confirmation_button = tk.RAISED
    inactive_player_confirmation_button = tk.SUNKEN
    player_labels = tk.SUNKEN

    # Historic info grid
    game_win_count_label = tk.SUNKEN
    player_win_count_label = tk.SUNKEN

