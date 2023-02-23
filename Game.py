class Game:
    def __init__(self, event, site, date, round, result, white_player, black_player, moves):
        self.event = event
        self.site = site
        self.date = date
        self.round = round
        self.result = result
        self.white_player = white_player
        self.black_player = black_player
        self.moves = moves

    def get_moves(self):
        return self.moves

    def set_moves(self, moves):
        self.moves = moves
    
    def __repr__(self):
        return f"(Round: {self.round}, Result: {self.result}, White Player: {self.white_player}, Black Player: {self.black_player})"