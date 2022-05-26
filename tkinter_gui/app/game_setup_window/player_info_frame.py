from game.constants.game_constants import BoardMarking, StartingPlayer
from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
from tkinter_gui.constants.dimensions import SetupWindowDimensions
from tkinter_gui.constants.game_parameter_constraints import GameParameterConstraint
import tkinter as tk
from math import floor


class PlayerInfoFrame:
    """Class for the frame that allows users to enter their names and say who should go first."""
    def __init__(self,
                 widget_manager: GameSetupWidgets,
                 player_x_entry: tk.StringVar = None,
                 player_o_entry: tk.StringVar = None,
                 starting_player: tk.IntVar = None):
        self.widget_manager = widget_manager
        self.player_x_entry = player_x_entry
        self.player_o_entry = player_o_entry
        self.starting_player = starting_player

    def populate_player_info_frame(self):
        """Method to add all components of the player info frame to the grid"""
        self._configure_player_info_frame()
        self._upload_entry_widgets_to_widget_manager()
        self._upload_radio_buttons_to_widget_manager()

        # Player naming
        player_x_label = self.get_player_label(player_x=True)
        player_o_label = self.get_player_label(player_x=False)
        player_x_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        player_o_label.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.widget_manager.player_x_entry.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.widget_manager.player_o_entry.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        starting_player_label = self.get_starting_player_label()
        starting_player_label.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=5, pady=1)
        self.widget_manager.random_player_starts_radio.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=1)
        self.widget_manager.player_x_starts_radio.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=1)
        self.widget_manager.player_o_starts_radio.grid(row=5, column=1, columnspan=2, sticky="ew", padx=5, pady=1)

    def _configure_player_info_frame(self):
        self.widget_manager.player_info_frame = tk.Frame(
            master=self.widget_manager.setup_window,
            background=Colour.player_info_frame_background.value,
            borderwidth=3, relief=Relief.player_info_frame.value,
        )
        self.widget_manager.player_info_frame.rowconfigure(
            index=[0, 1], minsize=floor(SetupWindowDimensions.player_info_frame.height / 5), weight=1)
        self.widget_manager.player_info_frame.columnconfigure(
            index=[0, 1], minsize=floor(SetupWindowDimensions.player_info_frame.width / 2), weight=1)

    def _upload_entry_widgets_to_widget_manager(self):
        """Method that adds all relevant widgets in the player info frame to the widget manager"""
        self.widget_manager.player_x_entry = self.get_player_entry_field(player_x=True)
        self.widget_manager.player_o_entry = self.get_player_entry_field(player_x=False)

    ##########
    # Player labels and entry
    ##########
    def get_player_label(self, player_x: bool) -> tk.Label:
        """
        Method returning the label showing player one / player two.
        Note these are just static labels so don't need to go in the widget manager
        """
        if player_x:
            marking = BoardMarking(1).name
        else:
            marking = BoardMarking(-1).name
        player_label = tk.Label(
            master=self.widget_manager.player_info_frame,
            text="Player: " + f"{marking}",
            background=Colour.player_info_labels.value,
            relief=Relief.player_info_labels.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height/12)),
            justify=tk.CENTER
        )
        return player_label

    def get_player_entry_field(self, player_x: bool) -> tk.Entry:
        """Method returning an entry field where players can write their names."""
        if player_x:
            self.player_x_entry = tk.StringVar()
            entry_text = self.player_x_entry
            entry_text.trace_add(mode="write", callback=self.character_limit)
        else:
            self.player_o_entry = tk.StringVar()
            entry_text = self.player_o_entry
            entry_text.trace_add(mode="write", callback=self.character_limit)
        player_name_entry = tk.Entry(
            master=self.widget_manager.player_info_frame,
            textvariable=entry_text,
            background=Colour.player_name_entry.value,
            relief=Relief.player_name_entry.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 12)),
            justify=tk.CENTER
        )
        return player_name_entry

    def character_limit(self, var, index, mode) -> None:
        """
        Trace function that gets added to the entry fields' variables, so that players cannot enter a name with length
        greater than the max player length
        Parameters:
        var - name of the tkinter variable the trace will be added to
        index - index of the tkinter variable in case it's an array
        mode - mode to trace the variable in i.e. read, write, etc.
        These are really just placeholders for the automatic positional args that get added by trace_add - could just
        use an *args but this makes it clearer what is going on.
        """
        if len(self.player_x_entry.get()) > GameParameterConstraint.max_player_length.value:
            self.player_x_entry.set(self.player_x_entry.get()[:GameParameterConstraint.max_player_length.value])
        elif len(self.player_o_entry.get()) > GameParameterConstraint.max_player_length.value:
            self.player_o_entry.set(self.player_o_entry.get()[:GameParameterConstraint.max_player_length.value])

    ##########
    # Starting player radio buttons
    ##########
    def get_starting_player_label(self) -> tk.Label:
        """Method that returns the label saying "choose starting player" above the radio buttons"""
        starting_player_label = tk.Label(
            master=self.widget_manager.player_info_frame,
            text="Choose who goes first",
            background=Colour.starting_player_label.value,
            relief=Relief.starting_player_label.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 20)))
        return starting_player_label

    def _upload_radio_buttons_to_widget_manager(self) -> None:
        self.starting_player = tk.IntVar(value=StartingPlayer.RANDOM.value)
        player_x_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Player X", variable=self.starting_player,
            value=StartingPlayer.PLAYER_X.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height/20)))
        self.widget_manager.player_x_starts_radio = player_x_starts
        player_o_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Player O", variable=self.starting_player,
            value=StartingPlayer.PLAYER_O.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height/20)))
        self.widget_manager.player_o_starts_radio = player_o_starts
        random_player_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Random", variable=self.starting_player,
            value=StartingPlayer.RANDOM.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height/20)))
        self.widget_manager.random_player_starts_radio = random_player_starts
