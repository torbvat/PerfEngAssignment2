class ChessGame:
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

    def getMoves(self):
        return self.moves

    def setMoves(self, moves):
        self.moves = moves

    def getEvent(self):
        return self.event
    
    def getSite(self):
        return self.site
    
    def getDate(self):
        return self.date
    
    def getRound(self):
        return self.round
    
    def getResult(self):
        return self.result
    
    def getEco(self):
        return self.eco
    
    def getOpening(self):  
        return self.opening
    
    def getPlyCount(self):
        return self.plycount
    
    def getWhitePlayer(self):
        return self.white_player
    
    def getBlackPlayer(self):
        return self.black_player
    
    def getVariation(self):
        return self.variation
    
    
    def __repr__(self):
        return f"(Round: {self.round}, Result: {self.result}, White Player: {self.white_player}, Black Player: {self.black_player})\n"



class ChessMove:
    def __init__(self, move_number, player, move_text):
        self.move_number = move_number
        self.player = player
        self.move_text = move_text

    def getMoveNumber(self):
        return self.move_number
    
    def getPlayer(self):
        return self.player
    
    def getMoveText(self):
        return self.move_text

    def __repr__(self):
        return f" Move Number: {self.move_number}, Move Text: {self.move_text}\n"

  
    
class ChessPlayer:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def getName(self):
        return self.name
    
    def getRating(self):
        return self.rating
    
    def __repr__(self):
        return f"[{self.name}, Rating: {self.rating}]"