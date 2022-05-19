from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.style_and_colours import GameColour, Font
import tkinter as tk
from math import floor
from functools import partial


class NoughtsAndCrossesWindow(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 player_o: Player,
                 player_x: Player,
                 starting_player: GameValue = GameValue.X,
                 active_unconfirmed_cell: (int, int) = None):
        super().__init__(game_rows_m, game_cols_n, win_length_k, player_o, player_x, starting_player)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.min_cell_height = floor(FrameDimensions.game_frame.height / game_rows_m)
        self.min_cell_width = floor(FrameDimensions.game_frame.width / game_cols_n)

    def launch_playing_window(self):
        """Method for launching the main noughts and crosses game play window and controlling the game flow"""
        # Define and configure the window
        game_window = tk.Tk()
        game_window.title("Noughts and Crosses")
        game_window.configure(background=GameColour.window.value)
        self.create_all_game_components(master_window=game_window)
        game_window.mainloop()

    def create_all_game_components(self, master_window: tk.Tk):
        # Background frame that contains all components of the game
        background_frame = tk.Frame(master=master_window, background=GameColour.background.value, borderwidth=3,
                                    relief=tk.RIDGE)
        background_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Frame that contains the playing grid (entire left)
        game_frame = tk.Frame(
            master=background_frame, background=GameColour.game_background.value,
            width=FrameDimensions.game_frame.width, height=FrameDimensions.game_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        game_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.create_playing_grid(master_frame=game_frame)

        # Frame for the buttons that control the gameplay (top-right)
        game_info_frame = tk.Frame(
            master=background_frame, background=GameColour.game_buttons_background.value,
            width=FrameDimensions.game_info_frame.width, height=FrameDimensions.game_info_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        game_info_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Frame for the labels that says the status across multiple games (bottom-right)
        historic_info_frame = tk.Frame(
            master=background_frame, background=GameColour.game_status_background.value,
            width=FrameDimensions.historic_info_frame.width, height=FrameDimensions.historic_info_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        historic_info_frame.grid(row=1, column=1, sticky="s", padx=10, pady=10)

    def create_playing_grid(self, master_frame: tk.Frame):

        """Loops over the playing grid and creates an analogous grid of fields/buttons."""
        master_frame.rowconfigure(index=list(range(0, self.game_rows_m)),
                                  minsize=self.min_cell_height,
                                  weight=1)
        master_frame.columnconfigure(index=list(range(0, self.game_cols_n)),
                                     minsize=self.min_cell_width,
                                     weight=1)
        for row in range(0, self.game_rows_m):
            for col in range(0, self.game_cols_n):
                if (row, col) == self.active_unconfirmed_cell:
                    print(f"Identified {row, col} as active unc cell")
                    unconfirmed_cell_choice_label = tk.Label(
                        master=master_frame,
                        text="X",  # TODO text is the active player piece
                        font=(Font.xo_font.value, floor(self.min_cell_height / 2)),
                        background=GameColour.unconfirmed_cell_colour.value, relief=tk.RAISED)
                    unconfirmed_cell_choice_label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                elif self.playing_grid[row, col] == 0:  # Cell is empty so user can enter an 0 / X
                    command_func = partial(self.update_playing_grid_unconfirmed, master_frame, (row, col))
                    available_cell_button = tk.Button(
                        master=master_frame,
                        command=command_func,
                        background=GameColour.empty_entry_cell.value, relief=tk.RAISED)
                    available_cell_button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                else:
                    text = GameValue(self.playing_grid[row, col]).name  # X or O
                    occupied_cell_label = tk.Label(
                        master=master_frame,
                        text=text,
                        font=(Font.xo_font.value, floor(self.min_cell_height / 2)),
                        background=GameColour.occupied_cell.value, relief=tk.SUNKEN)
                    occupied_cell_label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    def update_playing_grid_unconfirmed(self, master_frame: tk.Frame, new_cell_index: (int, int)):
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to a button.

        Note this all needs to be contained within one method so that it can be added as the command function for the
        available_cell_button.
        """
        # Replace rejected unconfirmed cell choice with selection button
        command_func = partial(self.update_playing_grid_unconfirmed, master_frame, (self.active_unconfirmed_cell[0],
                                                                                    self.active_unconfirmed_cell[1]))
        available_cell_button = tk.Button(
            master=master_frame,
            command=command_func,
            background=GameColour.empty_entry_cell.value, relief=tk.RAISED)
        available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                   column=self.active_unconfirmed_cell[1], sticky="nsew")

        # Set new unconfirmed cell to be the index and place a label in it
        self.active_unconfirmed_cell = new_cell_index
        unconfirmed_cell_choice_label = tk.Label(
            master=master_frame,
            text="X",  # TODO text is the active player piece
            font=(Font.xo_font.value, floor(self.min_cell_height / 2)),
            background=GameColour.unconfirmed_cell_colour.value, relief=tk.RAISED)
        unconfirmed_cell_choice_label.grid(row=self.active_unconfirmed_cell[0],
                                           column=self.active_unconfirmed_cell[1],
                                           sticky="nsew", padx=1, pady=1)

    def confirm_cell_choice(self):
        """Sets active_unconfirmed_cell to None"""
        pass

    def create_active_game_grid(self, master_frame: tk.Frame):
        """Populates a frame with a label showing who's turn it is, and a button to confirm entry"""
        pass
