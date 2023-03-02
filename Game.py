class Game:
    def __init__(self, event, site, date, round, result, eco, opening, plycount, white_player, black_player, moves, variation):
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
        self.variation = variation

    def get_moves(self):
        return self.moves

    def set_moves(self, moves):
        self.moves = moves

    def get_event(self):
        return self.event
    
    def get_site(self):
        return self.site
    
    def get_date(self):
        return self.date
    
    def get_round(self):
        return self.round
    
    def get_result(self):
        return self.result
    
    def get_eco(self):
        return self.eco
    
    def get_opening(self):  
        return self.opening
    
    def get_plycount(self):
        return self.plycount
    
    def get_white_player(self):
        return self.white_player
    
    def get_black_player(self):
        return self.black_player
    
    def get_variation(self):
        return self.variation
    
    
    def __repr__(self):
        return f"(Round: {self.round}, Result: {self.result}, White Player: {self.white_player}, Black Player: {self.black_player})\n"