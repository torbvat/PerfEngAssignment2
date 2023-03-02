class Game:
    def __init__(self, event, site, date, round, result, eco, opening, plycount, white_player, black_player, moves, variation = None):
        self.event = event
        self.site = site
        self.date = date
        self.round = round
        self.result = result
        self.eco = eco
        self.opening = opening
        self.plycount = plycount
        self.white_player = white_player
        self.black_player = black_player
        self.moves = moves
        self.varation = variation

    def get_moves(self):
        return self.moves

    def set_moves(self, moves):
        self.moves = moves
    
    def __repr__(self):
        return f"(Round: {self.round}, Result: {self.result}, White Player: {self.white_player}, Black Player: {self.black_player})\n"