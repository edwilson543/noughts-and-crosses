from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.style_and_colours import Colour
from tkinter_gui.app.main_game_window.active_game_frames import NoughtsAndCrossesGameFrames
import tkinter as tk
from math import floor


#  TODO whether need to destroy replaced widgets, for fine to judt grid in a new one

class NoughtsAndCrossesWindow(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue = GameValue.X,
                 active_unconfirmed_cell: (int, int) = None):
        super().__init__(game_rows_m, game_cols_n, win_length_k, pos_player, neg_player, starting_player)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.game_frames = NoughtsAndCrossesGameFrames
        self.min_cell_height = floor(FrameDimensions.game_frame.height / game_rows_m)
        self.min_cell_width = floor(FrameDimensions.game_frame.width / game_cols_n)

    def launch_playing_window(self):
        """Method for launching the main noughts and crosses game play window and controlling the game flow"""
        # Define and configure the window
        game_window = tk.Tk()
        game_window.title("Noughts and Crosses")
        game_window.configure(background=Colour.window.value)
        self.create_all_game_components(master_window=game_window)
        game_window.mainloop()

    def create_all_game_components(self, master_window: tk.Tk):
        """Method to create all the frames used in the main game window and fill the with their components"""
        # Background frame that contains all components of the game
        background_frame = tk.Frame(master=master_window, background=Colour.background.value, borderwidth=3,
                                    relief=tk.RIDGE)
        background_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        background_frame.rowconfigure(index=[0, 1], minsize=FrameDimensions.game_frame.height/2, weight=1)
        background_frame.columnconfigure(index=0, minsize=FrameDimensions.game_frame.width, weight=1)
        background_frame.columnconfigure(index=1, minsize=FrameDimensions.game_info_frame.width, weight=1)

        # Frame that contains the playing grid (entire left)
        game_frame = tk.Frame(
            master=background_frame, background=Colour.game_background.value,
            width=FrameDimensions.game_frame.width, height=FrameDimensions.game_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        game_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        active_game_frames_carrier = self.get_active_game_frames_object()
        active_game_frames_carrier.populate_empty_playing_grid(master_frame=game_frame)

        # Frame for the buttons that control the gameplay (top-right)
        game_info_frame = tk.Frame(
            master=background_frame, background=Colour.game_buttons_background.value,
            width=FrameDimensions.game_info_frame.width, height=FrameDimensions.game_info_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        game_info_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        active_game_frames_carrier.populate_game_info_grid(master_frame=game_info_frame, playing_grid_frame=game_frame)

        # Frame for the labels that says the status across multiple games (bottom-right)
        historic_info_frame = tk.Frame(
            master=background_frame, background=Colour.game_status_background.value,
            width=FrameDimensions.historic_info_frame.width, height=FrameDimensions.historic_info_frame.height,
            borderwidth=5, relief=tk.SUNKEN)
        historic_info_frame.grid(row=1, column=1, sticky="s", padx=10, pady=10)

    def get_active_game_frames_object(self) -> NoughtsAndCrossesGameFrames:
        """Method to instantiate the object that carries the active game frames"""
        game_frames_carrier = NoughtsAndCrossesGameFrames(
            game_rows_m=self.game_rows_m,
            game_cols_n=self.game_cols_n,
            win_length_k=self.win_length_k,
            pos_player=self.pos_player,
            neg_player=self.neg_player,
            starting_player=self.starting_player
        )
        return game_frames_carrier
