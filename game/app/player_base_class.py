from game.constants.game_constants import GameValue

class Player:
    """Class for the players of the noughts and crosses game."""

    def __init__(self,
                 name: str,
                 active_symbol: GameValue,
                 active_game_win_count: int = 0):
        self.name = name
        self.active_symbol = active_symbol
        self.active_game_win_count = active_game_win_count

    def award_point(self):
        """Method to award the player a point."""
        self.active_game_win_count += 1
