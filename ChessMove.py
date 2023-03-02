class ChessMove:
    def __init__(self, move_number, player, move_text):
        self.move_number = move_number
        self.player = player
        self.move_text = move_text

    def get_move_number(self):
        return self.move_number
    
    def get_player(self):
        return self.player
    
    def get_move_text(self):
        return self.move_text

    def __repr__(self):
        return f" Move Number: {self.move_number}, Move Text: {self.move_text}\n"