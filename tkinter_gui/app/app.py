from tkinter_gui.app.main_game_window.main_game_window import PlayingWindow
from tkinter_gui.app.game_setup_window.game_setup_window import SetupWindow


#  TODO random choice is not going to work, so update this

class NoughtsAndCrossesApp(SetupWindow):
    def __init__(self, setup_parameters=None):
        super().__init__(setup_parameters)

    def launch_game(self):
        super().launch_setup_window()
        playing_window = PlayingWindow(setup_parameters=self.setup_parameters)
        playing_window.launch_playing_window()

NoughtsAndCrossesApp().launch_game()




