""" 
Created by: Torbjørn Vatne and Erlend Nygaard Kristiansen
Group 18
"""
class ChessGame:
    def __init__(self, event, site, date, round, result, eco, opening, plycount, whitePlayer, blackPlayer, moves, variation):
        self.event = event
        self.site = site
        self.date = date
        self.round = round
        self.result = result
        self.eco = eco
        self.opening = opening
        self.plycount = plycount
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
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
        return self.whitePlayer
    
    def getBlackPlayer(self):
        return self.blackPlayer
    
    def getVariation(self):
        return self.variation
    
    
    def __repr__(self):
        return f"(Round: {self.round}, Result: {self.result}, White Player: {self.whitePlayer}, Black Player: {self.blackPlayer})\n"



class ChessMove:
    def __init__(self, moveNumber, player, moveText):
        self.moveNumber = moveNumber
        self.player = player
        self.moveText = moveText

    def getMoveNumber(self):
        return self.moveNumber
    
    def getPlayer(self):
        return self.player
    
    def getMoveText(self):
        return self.moveText

    def __repr__(self):
        return f" Move Number: {self.moveNumber}, Move Text: {self.moveText}\n"

  
    
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