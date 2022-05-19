from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.colours import GameColour
import tkinter as tk


class NoughtsAndCrossesWindow(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 player_o: Player,
                 player_x: Player,
                 starting_player: GameValue = GameValue.X):
        super().__init__(game_rows_m, game_cols_n, win_length_k, player_o, player_x, starting_player)

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
        min_cell_width = FrameDimensions.game_frame.width / self.game_cols_n
        min_cell_height = FrameDimensions.game_frame.height / self.game_rows_m
        master_frame.rowconfigure(index=list(range(0, self.game_rows_m)),
                                  minsize=min_cell_height,
                                  weight=1)
        master_frame.columnconfigure(index=list(range(0, self.game_cols_n)),
                                     minsize=min_cell_width,
                                     weight=1)
        for row in range(0, self.game_rows_m):
            for col in range(0, self.game_cols_n):
                if self.playing_grid[row, col] == 0:  # Cell is empty so user can enter an 0 / X
                    cell_entry = tk.Button(master=master_frame,
                                          background=GameColour.empty_entry_cell.value)
                    cell_entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                else:
                    text = GameValue(self.playing_grid[row, col]).name  # X or O
                    cell_entry = tk.Label(master=master_frame,
                                          text=text,
                                          background=GameColour.full_cell.value)
                    cell_entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    def create_active_game_grid(self, master_frame: tk.Frame):
        """Populates a frame with a label showing who's turn it is, and a button to confirm entry"""



