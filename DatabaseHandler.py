""" 
Created by: Torbjørn Vatne and Erlend Nygaard Kristiansen
Group 18
"""
import Chess #Class for storing data about a single move, player, and game
import re
class DatabaseHandler:
    def __init__(self, filePath):
        self.filePath = filePath

    def readGames(self, numberOfGames = None):
        gameCount = 0
        games = []
        moves = []
        moveString = ""
        with open(self.filePath, 'r') as file:
            event = site = date = round = result = eco = opening  = plycount = None
            whiteName = whiteElo = blackName = blackElo = None
            variation = "Standard"
            for line in file:
                if line is None or line=="\n" or line == " " or line == "":
                    continue
                elif line.startswith('[Event'):
                    if gameCount == numberOfGames: #If we have read the number of games we want to read, stop reading
                        break
                    moves = []
                    gameCount += 1
                    event = line.split('"')[1]
                elif line.startswith('[Site '):
                    site = line.split('"')[1]
                elif line.startswith('[Date '):
                    date = line.split('"')[1]
                elif line.startswith('[Round '):
                    round = line.split('"')[1]
                elif line.startswith('[White '):
                    whiteName = line.split('"')[1]
                elif line.startswith('[Black '):
                    blackName = line.split('"')[1]
                elif line.startswith('[Result '):
                    result = line.split('"')[1]
                elif line.startswith('[ECO '):
                    eco = line.split('"')[1]
                elif line.startswith('[Opening '):
                    opening = line.split('"')[1]
                elif line.startswith('[Variation '):
                    variation = line.split('"')[1]
                elif line.startswith('[PlyCount '):
                    plycount = line.split('"')[1]
                elif line.startswith('[WhiteElo '):
                    whiteElo = line.split('"')[1]
                elif line.startswith('[BlackElo '):
                    blackElo = line.split('"')[1]
                else:
                    moveString += line.strip("\n")
                    
                if moveString.endswith("1-0") or moveString.endswith("0-1") or moveString.endswith("1/2-1/2"):
                    whitePlayer = Chess.ChessPlayer(whiteName, whiteElo)
                    blackPlayer = Chess.ChessPlayer(blackName, blackElo)
                    moveString = moveString.replace(".", " ") #Replace all periods with spaces to seperate moves and move numbers when creating a list
                    moveElements = re.findall(r'\S+', re.sub(r'{.*?}', '', moveString)) #Remove comments and creates a list of all elements in moveString
                    for i in range(0, len(moveElements)-2, 3):
                        if moveElements[i+2] == "1-0" or moveElements[i+2] == "0-1" or moveElements[i+2] == "1/2-1/2":
                            whiteMove = Chess.ChessMove(moveElements[i].strip("."), whitePlayer, moveElements[i+1])
                            moves.append(whiteMove)
                            break
                        moveNumber = moveElements[i].strip(".")
                        moveStrWhite = moveElements[i+1]
                        moveStrBlack = moveElements[i+2]
                        blackMove = Chess.ChessMove(moveNumber, blackPlayer, moveStrBlack)
                        whiteMove = Chess.ChessMove(moveNumber, whitePlayer, moveStrWhite)
                        
                        moves.append(whiteMove)
                        moves.append(blackMove)
                    moveString = ""
                    games.append(Chess.ChessGame(event, site, date, round, result, eco, opening, plycount, whitePlayer, blackPlayer, moves, variation))
        return games
    
    def writeToFile(self, Games, filePath):
        with open(filePath, 'w') as file:
            for game in Games:
                moveCounter = 0
                file.write("[Event\t" + game.getEvent() + "]\n")
                file.write("[Site\t" + game.getSite() + "]\n")
                file.write("[Date\t" + game.getDate() + "]\n")
                file.write("[Round\t" + game.getRound() + "]\n")
                file.write("[White\t" + game.getWhitePlayer().getName() + "]\n")
                file.write("[Black\t" + game.getBlackPlayer().getName() + "]\n")
                file.write("[Result\t" + game.getResult() + "]\n")
                file.write("[ECO\t" + game.getEco() + "]\n")
                file.write("[Opening\t" + game.getOpening() + "]\n")
                file.write("[Variation\t" + game.getVariation() + "]\n")
                file.write("[PlyCount\t" + game.getPlyCount() + "]\n")
                file.write("[WhiteElo\t" + game.getWhitePlayer().getRating() + "]\n")
                file.write("[BlackElo\t" + game.getBlackPlayer().getRating() + "]\n")
                file.write("\n")
                for i in range(0, len(game.getMoves()), 2):
                    moveCounter += 1
                    if i+2 == len(game.getMoves()):
                        file.write(str(game.getMoves()[i].getMoveNumber()) + ". " + game.getMoves()[i].getMoveText() + " " + game.getMoves()[i+1].getMoveText() + " " + game.getResult() + "\n\n")
                    elif i+1 < len(game.getMoves()):
                        file.write(str(game.getMoves()[i].getMoveNumber()) + ". " + game.getMoves()[i].getMoveText() + " " + game.getMoves()[i+1].getMoveText()+ " ")
                    elif i+1 == len(game.getMoves()):
                        file.write(str(game.getMoves()[i].getMoveNumber()) + ". " + game.getMoves()[i].getMoveText() + " " + game.getMesult() + "\n\n")
                    else: 
                        file.write(str(game.getMoves()[i].getMoveNumber()) + ". " + game.getMoves()[i].getMoveText() + " " + game.getMesult() + "\n\n")
                    if moveCounter % 4 == 0:
                        file.write("\n")
                if moveCounter % 4 != 0:
                    file.write("\n\n")


    
    