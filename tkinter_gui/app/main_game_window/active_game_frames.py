from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
import tkinter as tk
from math import floor
from functools import partial
import logging


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
    # Methods populating the two frames with the relevant buttons
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
        self.playing_grid_widget_dict = {}
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                                   row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.playing_grid_widget_dict[(row_index, col_index)] = available_cell_button

    def populate_game_info_grid(self, master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> None:
        """
        Method that populates the game info grid with a confirmation button, and indication of who's turn it is.

        Parameters:
        ----------
        mater_frame: The frame that this grid will be packed into
        playing_grid_frame: The playing grid frame - the confirmation button must be able to communicate with the
        info grid.

        Returns: None

        """
        master_frame.rowconfigure(index=[0, 1, 2], minsize=floor(FrameDimensions.game_info_frame.height / 3))
        master_frame.columnconfigure(index=[0, 1, 2], minsize=floor(FrameDimensions.game_info_frame.width / 3))

        confirm_cell_choice_button = self.confirm_cell_choice_button(button_master_frame=master_frame,
                                                                     playing_grid_frame=playing_grid_frame)
        confirm_cell_choice_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        player_turn_label = self.player_turn_label(master_frame=master_frame)
        player_turn_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        pos_player_label = self.player_label(master_frame=master_frame, player=self.pos_player)
        pos_player_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        neg_player_label = self.player_label(master_frame=master_frame, player=self.neg_player)
        neg_player_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        # TODO add remaining features and format

    ##########
    # Labels/ buttons on the playing grid
    ##########

    def occupied_cell_label(self, master_frame: tk.Frame) -> tk.Label:
        """Label widget that shows that a cell is already occupied and displays the relevant marking."""
        text = self.get_player_turn_marking()
        colour = self.get_occupied_cell_colour(marking=text)
        occupied_cell_label = tk.Label(
            master=master_frame,
            text=text,  # X or O
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=colour, relief=Relief.occupied_cell.value)
        return occupied_cell_label

    def unconfirmed_cell_button(self, master_frame: tk.Frame) -> tk.Button:
        """Label widget that shows that a cell has temporarily been selected as the player's move."""
        command_func = partial(self.unconfirmed_cell_choice_button_command, master_frame)
        text = self.get_player_turn_marking()
        unconfirmed_cell_choice_button = tk.Button(
            master=master_frame,
            command=command_func,
            text=text,
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=Colour.unconfirmed_cell.value, relief=Relief.unconfirmed_cell.value,
            foreground=Colour.unconfirmed_cell_font.value)
        return unconfirmed_cell_choice_button

    def available_cell_button(self, master_frame: tk.Frame, row_index: int, col_index: int) -> tk.Button:
        """Button widget that shows that a cell is available for selection"""
        command_func = partial(self.available_cell_button_command, master_frame, row_index, col_index)
        available_cell_button = tk.Button(
            master=master_frame,
            command=command_func,
            background=Colour.available_cell.value, relief=Relief.available_cell.value)
        return available_cell_button

    ##########
    # Commands for buttons on the playing grid
    ##########
    def available_cell_button_command(self, master_frame: tk.Frame, row_index: int, col_index: int) -> None:
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to a button.

        Note this all needs to be contained within one method so that it can be added as the command function for the
        available_cell_button.
        """
        logging.info(f"Available cell button clicked at {row_index, col_index}")
        # Activate the confirmation button
        self.playing_grid_widget_dict["CONFIRMATION"]["state"] = tk.NORMAL

        logging.info(f"Existing active unconfirmed cell: {self.active_unconfirmed_cell}")
        if self.active_unconfirmed_cell is not None:
            # Destroy existing active unconfirmed cell choice button
            self.playing_grid_widget_dict[self.active_unconfirmed_cell].destroy()

            # Replace destroyed unconfirmed cell choice button with an available cell button
            available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                               row_index=self.active_unconfirmed_cell[0],
                                                               col_index=self.active_unconfirmed_cell[1])
            available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                       column=self.active_unconfirmed_cell[1], sticky="nsew")
            self.playing_grid_widget_dict[self.active_unconfirmed_cell] = available_cell_button
            logging.info(f"New available cell button created at: {row_index, col_index}")

        # Set new unconfirmed cell to be the index, and place an unconfirmed cell choice button in it
        self.active_unconfirmed_cell = (row_index, col_index)
        unconfirmed_cell_choice_button = self.unconfirmed_cell_button(master_frame=master_frame)
        unconfirmed_cell_choice_button.grid(row=self.active_unconfirmed_cell[0],
                                            column=self.active_unconfirmed_cell[1],
                                            sticky="nsew", padx=1, pady=1)
        self.playing_grid_widget_dict[self.active_unconfirmed_cell] = unconfirmed_cell_choice_button
        logging.info(f"New unconfirmed cell created at: {self.active_unconfirmed_cell}")

    def unconfirmed_cell_choice_button_command(self, master_frame: tk.Frame) -> None:
        """
        Method to define what happens when the unconfirmed cell choice button is clicked.
        An available cell button is inserted in place of the unconfirmed cell choice button.
        Also, the active_unconfirmed_cell is set to None as there is no longer an active unconfirmed cell.

        Purpose:
        1) Two clicks on an empty cell highlights and then un-highlights that cell
        2) To be part of the command when a new available cell is chosen as the active unconfirmed cell (i.e. first have
        to remove the existing unconfirmed cell)
        """

        logging.info(f"Unconfirmed cell choice button clicked at {self.active_unconfirmed_cell}")

        # Destroy existing unconfirmed cell choice button
        self.playing_grid_widget_dict[self.active_unconfirmed_cell].destroy()

        # Replace destroyed unconfirmed cell choice button with an available cell choice button
        available_cell_button = self.available_cell_button(master_frame=master_frame,
                                                           row_index=self.active_unconfirmed_cell[0],
                                                           col_index=self.active_unconfirmed_cell[1])
        available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                   column=self.active_unconfirmed_cell[1], sticky="nsew")
        self.playing_grid_widget_dict[self.active_unconfirmed_cell] = available_cell_button
        logging.info(f"New available cell button created at {self.active_unconfirmed_cell}")

        # Indicate that there is now no active unconfirmed cell and disable confirmation button
        self.active_unconfirmed_cell = None
        self.playing_grid_widget_dict["CONFIRMATION"]["state"] = tk.DISABLED

    ##########
    # Buttons and labels relating to the game_info_grid
    ##########

    def confirm_cell_choice_button(self, button_master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> tk.Button:
        """
        Parameters:
        __________

        Returns:
        __________
        """
        command_func = partial(self.confirm_cell_choice_button_command, button_master_frame, playing_grid_frame)
        confirm_cell_choice_button = tk.Button(
            master=button_master_frame,
            command=command_func,
            state=tk.DISABLED,
            background=Colour.unconfirmed_cell.value,
            foreground=Colour.info_panels_font.value,
            font=(Font.info_panels.value, floor(FrameDimensions.game_info_frame.height / 10)),
            text="Confirm\nSelection")

        self.playing_grid_widget_dict["CONFIRMATION"] = confirm_cell_choice_button
        return confirm_cell_choice_button

    @staticmethod
    def player_turn_label(master_frame: tk.Frame) -> tk.Label:
        """
        Method to create a label that says "Player turn" above the coloured labels indicating who's turn it is.
        """
        player_turn_label = tk.Label(master=master_frame,
                                     text="Player's Turn:",
                                     relief=Relief.players_turn.value,
                                     background=Colour.players_turn_label.value,
                                     font=(Font.info_panels.value, floor(FrameDimensions.game_info_frame.height / 10)))
        return player_turn_label

    def player_label(self, master_frame: tk.Frame, player: Player) -> tk.Label:
        """
        Method to create the player label's and show who's turn it is to mark the board
        """
        x_or_o = GameValue(player.active_symbol).name
        text = f"{player.name}:\n{x_or_o}"
        colour = self.get_player_label_colour(player=player)
        relief = self.get_player_label_relief(player=player)
        player_label = tk.Label(master=master_frame,
                                text=text,
                                background=colour,
                                font=(Font.info_panels.value, floor(FrameDimensions.game_info_frame.height / 10)),
                                relief=relief)
        self.playing_grid_widget_dict[f"{player.name}"] = player_label  # So the colour can be changed
        return player_label

    ##########
    # Command function for the confirmation button in the game info grid
    ##########

    def confirm_cell_choice_button_command(self, button_master_frame: tk.Frame, playing_grid_frame: tk.Frame) -> None:
        """
        Method to:
        1) Permanently marks the board as shown in the active unconfirmed cell.
        2) Updates the backend board (the -1s, 0s and 1s)
        3) Sets active_unconfirmed_cell to None
        4) Switch which player's label is highlighted/raised

        Parameters:
        ___________
        button_master_frame: The frame that the confirm cell choice button is located in
        playing_grid_frame: The frame that all of the playing cells are located in

        Returns: None
        """

        # Reset the cell choice button to disabled
        self.playing_grid_widget_dict["CONFIRMATION"]["state"] = tk.DISABLED

        # Permanently mark the board as shown in the active unconfirmed cell
        occupied_cell_label = self.occupied_cell_label(master_frame=playing_grid_frame)
        occupied_cell_label.grid(row=self.active_unconfirmed_cell[0], column=self.active_unconfirmed_cell[1],
                                 sticky="nsew")
        self.mark_board(row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None

        # Switch which player's label is highlighted
        pos_player_label = self.playing_grid_widget_dict[f"{self.pos_player.name}"]
        neg_player_label = self.playing_grid_widget_dict[f"{self.neg_player.name}"]

        pos_player_label.configure(background=self.get_player_label_colour(player=self.pos_player),
                                   relief=self.get_player_label_relief(player=self.pos_player))
        neg_player_label.configure(background=self.get_player_label_colour(player=self.neg_player),
                                   relief=self.get_player_label_relief(player=self.neg_player))

    # Lower level methods used for formatting
    def get_player_turn_marking(self) -> str:
        """Method to extract the player turn from the game baseclass as a 1/-1 and return it as an X or O."""
        turn_int = self.get_player_turn()
        return GameValue(turn_int).name

    @staticmethod
    def get_occupied_cell_colour(marking: str) -> str:
        """Method to take an X or O and then select the relevant colour"""
        if marking == "X":
            return Colour.occupied_cell_x.value
        else:
            return Colour.occupied_cell_o.value

    def get_player_label_colour(self, player: Player) -> str:
        """Highlights the player's label if it's there go, otherwise their label is not highlighted."""
        if self.get_player_turn() == player.active_symbol.value:
            return Colour.unconfirmed_cell.value
        else:
            return self.get_occupied_cell_colour(marking=GameValue(player.active_symbol).name)

    def get_player_label_relief(self, player: Player):
        """Raises the player's label if it's there go, otherwise their label is sunken."""
        if self.get_player_turn() == player.active_symbol.value:
            return Relief.active_player_label.value
        else:
            return Relief.inactive_player_label.value
