import tkinter as tk

#  COLOURS
background_col = "black"
game_background = "#d1c7c7"

game_buttons_background = "blue"
game_status_background = "green"

board_rows = 3
board_cols = 3


# Define and configure the window
window = tk.Tk()
window.title("Noughts and Crosses")
window.configure(background=background_col)

# Background frame that should captures everything
background_frame = tk.Frame(master=window, background=background_col, width=750, height=500, borderwidth=3,
                            relief=tk.RIDGE)
background_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Game frame that contains the playing board
game_frame = tk.Frame(master=background_frame, background=game_background, width=750, height=300, borderwidth=5,
                      relief=tk.SUNKEN)
game_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

# Buttons frame that control the gameplay
game_buttons_frame = tk.Frame(master=background_frame, background=game_buttons_background, width=300, height=250,
                              borderwidth=5, relief=tk.SUNKEN)
game_buttons_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

# Frame for the labels that says the status across multiple games
game_status_frame = tk.Frame(master=background_frame, background=game_status_background, width=300, height=250,
                              borderwidth=5, relief=tk.SUNKEN)
game_status_frame.grid(row=1, column=1, sticky="s", padx=10, pady=10)

window.mainloop()

