class ChessMove:
    def __init__(self, move_number, player, move_text):
        self.move_number = move_number
        self.player = player
        self.move_text = move_text

    def __repr__(self):
        return f"Player: {self.player}, Move Number: {self.move_number}, Move Text: {self.move_text}"