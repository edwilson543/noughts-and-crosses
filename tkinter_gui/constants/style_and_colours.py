from enum import Enum
import tkinter as tk

# TODO could add array light/dark theme


class Colour(Enum):
    ##########
    # Main main_window
    ##########
    main_window = "black"
    main_frame_background = "black"

    # Inside the frames on the mian main_window
    game_background = "#d1c7c7"
    game_buttons_background = "#b2d1f7"
    game_status_background = "#78f599"

    # Inside the playing grid
    available_cell = "#fffad6"
    occupied_cell_o = "#dedede"
    occupied_cell_x = "#8c8b8b"
    winning_cell_flash_one = "#fdff7a"
    winning_cell_flash_two = "#e98deb"
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

    # Game continuation pop up
    pop_up_window_background = "black"
    game_outcome_label = "black"
    game_outcome_label_font = "white"
    game_continuation_exit_buttons = "#aff0eb"
    game_continuation_exit_buttons_font = "black"

    ##########
    # Game setup main window
    confirmation_button = "#b3bdbc"
    ##########

    # Game setup_parameters frame
    setup_window_background = "black"
    game_parameters_frame_background = "black"
    col_scale_background = "#8e9aad"
    col_scale_trough = "#79acfc"
    row_scale_background = "#800900"
    row_scale_trough = "#ffa59e"
    win_scale_background = "#a4fcae"
    win_scale_trough = "#28ad37"

    # Player info frame
    player_info_frame_background = "black"
    player_info_labels = "#9ec4e6"
    player_name_entry = "white"
    player_is_computer_checkbuttons = "#c2ffc8"
    starting_player_label = "#acad76" # Also used for the pop up
    starting_player_radio = "#fcffa1"  # Also used for the pop up


class Font(Enum):
    xo_font = "Times New Roman"
    default_font = "Times New Roman"


class Relief(Enum):
    ##########
    # Main game window
    ##########
    # Playing grid
    playing_grid_frame = tk.SUNKEN
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

    # Game continuation pop up
    game_outcome_label = tk.SUNKEN
    game_continuation_exit_buttons = tk.RAISED

    ##########
    # Game setup main_window
    ##########
    confirmation_button = tk.RAISED
    # Game setup_parameters frame
    game_parameters_frame = tk.RIDGE
    row_col_win_labels = tk.RIDGE

    # Player info frame
    player_info_frame = tk.RIDGE
    player_info_labels = tk.GROOVE
    player_name_entry = tk.SUNKEN
    starting_player_label = tk.RIDGE  # Also used for the pop up
    starting_player_radio = tk.RAISED  # Also used for the pop up
