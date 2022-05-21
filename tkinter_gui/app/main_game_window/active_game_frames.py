from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.style_and_colours import GameColour, Font
import tkinter as tk
from math import floor
from functools import partial


#  TODO whether need to destroy replaced widgets, for fine to judt grid in a new one

class NoughtsAndCrossesGameFrames(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue = GameValue.X,
                 active_unconfirmed_cell: (int, int) = None,
                 playing_grid_widget_dict: dict = None):
        super().__init__(game_rows_m, game_cols_n, win_length_k, pos_player, neg_player, starting_player)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.playing_grid_widget_dict = playing_grid_widget_dict
        self.min_cell_height = floor(FrameDimensions.game_frame.height / game_rows_m)
        self.min_cell_width = floor(FrameDimensions.game_frame.width / game_cols_n)

    ##########
    # Methods relating specifically to the playing grid
    # TODO this could just be all the populating methods up top
    ##########
    def populate_empty_playing_grid(self, master_frame: tk.Frame):

        """
        Loops over the playing grid and creates an analogous grid of selection buttons.
        Note that this is only called once at the start of the game, so all cells are empty.
        """
        master_frame.rowconfigure(index=list(range(0, self.game_rows_m)),
                                  minsize=self.min_cell_height,
                                  weight=1)
        master_frame.columnconfigure(index=list(range(0, self.game_cols_n)),
                                     minsize=self.min_cell_width,
                                     weight=1)
        playing_grid_widget_dict = {}
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                                   row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                playing_grid_widget_dict[(row_index, col_index)] = available_cell_button

    # Labels/ buttons on the playing grid
    def occupied_cell_label(self, master_frame: tk.Frame) -> tk.Label:
        """Label widget that shows that a cell is already occupied and displays the relevant marking."""
        occupied_cell_label = tk.Label(
            master=master_frame,
            text=self.get_player_turn_marking(),  # X or O
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=GameColour.occupied_cell.value, relief=tk.SUNKEN)
        return occupied_cell_label

    def unconfirmed_cell_choice_button(self, master_frame: tk.Frame) -> tk.Button:
        """Label widget that shows that a cell has temporarily been selected as the player's move."""
        command_func = partial(self.unconfirmed_cell_choice_button_command, master_frame)
        unconfirmed_cell_choice_button = tk.Button(
            master=master_frame,
            command=command_func,
            text=self.get_player_turn_marking(),
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=GameColour.unconfirmed_cell_colour.value, relief=tk.RAISED)
        return unconfirmed_cell_choice_button

    def available_cell_button(self, master_frame: tk.Frame, row_index: int, col_index: int) -> tk.Button:
        """Button widget that shows that a cell is available for selection"""
        command_func = partial(self.available_cell_button_command, master_frame, row_index, col_index)
        available_cell_button = tk.Button(
            master=master_frame,
            command=command_func,
            background=GameColour.empty_entry_cell.value, relief=tk.RAISED)
        return available_cell_button

    # Commands for buttons on the playing grid
    def available_cell_button_command(self, master_frame: tk.Frame, row_index: int, col_index: int) -> None:
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to a button.

        Note this all needs to be contained within one method so that it can be added as the command function for the
        available_cell_button.
        """

        # Replace rejected unconfirmed cell choice with available cell button
        if self.active_unconfirmed_cell is not None:
            available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                               row_index=row_index, col_index=col_index)
            available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                       column=self.active_unconfirmed_cell[1], sticky="nsew")

        # Set new unconfirmed cell to be the index and place a label in it
        self.active_unconfirmed_cell = (row_index, col_index)
        unconfirmed_cell_choice_button = self.unconfirmed_cell_choice_button(master_frame=master_frame)
        unconfirmed_cell_choice_button.grid(row=self.active_unconfirmed_cell[0],
                                            column=self.active_unconfirmed_cell[1],
                                            sticky="nsew", padx=1, pady=1)

    def unconfirmed_cell_choice_button_command(self, master_frame: tk.Frame) -> None:
        """
        Method to define what happens when the unconfirmed cell choice button is clicked.
        An available cell button is inserted in place of the unconfirmed cell choice button.
        Also, the active_unconfirmed_cell is set to None as there is no longer an active unconfirmed cell.

        Purpose:
        1) Two clicks on an empty cell highlights and then unhighlights that cell
        2) To be part of the command when a new available cell is chosen as the active unconfirmed cell (i.e. first have
        to remove the existing unconfirmed cell)
        """
        available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                           row_index=self.active_unconfirmed_cell[0],
                                                           col_index=self.active_unconfirmed_cell[1])
        available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                   column=self.active_unconfirmed_cell[1], sticky="nsew")
        #  TODO confirm choice button becomes a label when there is no unconfirmed cell
        self.active_unconfirmed_cell = None

    ##########
    # Methods relating to the game info grid
    ##########

    def populate_game_info_grid(self, master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> None:
        """
        Parameters:
        ----------

        Returns: None

        Outcomes:
        Adds confirmation button and player turn info to grid
        """
        master_frame.rowconfigure(index=[0, 1], minsize=FrameDimensions.game_info_frame.height / 2)
        master_frame.columnconfigure(index=0, minsize=FrameDimensions.game_info_frame.width)
        confirm_cell_choice_button = self.confirm_cell_choice_button(button_master_frame=master_frame,
                                                                     playing_grid_frame=playing_grid_frame)
        confirm_cell_choice_button.grid(row=1, column=0)
        # TODO add remaining features and format

    def confirm_cell_choice_button(self, button_master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> tk.Button:
        """
        Parameters:
        __________

        Returns:
        __________
        """
        command_func = partial(self.confirm_cell_choice_button_command, button_master_frame, playing_grid_frame)
        confirm_cell_choice_button = tk.Button(master=button_master_frame,
                                               command=command_func,
                                               # state=tk.DISABLED, # TODO
                                               text="Confirm\nSelection")
        # TODO format the button
        return confirm_cell_choice_button

    def confirm_cell_choice_button_command(self, button_master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> None:
        """
        Parameters:
        ___________

        Returns: None

        Outcomes:
        _________
        Permanently marks the board as shown in the active unconfirmed cell.
        Updates the backend board (the -1s, 0s and 1s)
        Sets active_unconfirmed_cell to None

        # TODO sets the confirmation button to be back to a label
        """
        occupied_cell_label = self.occupied_cell_label(master_frame=playing_grid_frame)
        occupied_cell_label.grid(row=self.active_unconfirmed_cell[0], column=self.active_unconfirmed_cell[1],
                                 sticky="nsew")
        print(self.playing_grid)
        self.mark_board(row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None

    def create_active_game_grid(self, master_frame: tk.Frame):
        """Populates a frame with a label showing who's turn it is, and a button to confirm entry"""
        pass

    # Lower level methods used throughout
    def get_player_turn_marking(self) -> str:
        """Method to extract the player turn from the game baseclass as a 1/-1 and return it as an X or O."""
        turn_int = self.get_player_turn()
        return GameValue(turn_int).name
