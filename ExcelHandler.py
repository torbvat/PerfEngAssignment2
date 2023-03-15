""" 
Created by: Torbjørn Vatne and Erlend Nygaard Kristiansen
Group 18
"""

import pandas as pd
import Chess

def exportGameToExcel(game, filePath):
    data = {
        "Move Number": [move.getMoveNumber() for move in game.getMoves()],
        "Move": [move.getMoveText() for move in game.getMoves()],
        "Meta Data": ["Event: " + game.getEvent(),
                        "Site: " + game.getSite(),
                        "Date: " + game.getDate(),
                        "Round: " + game.getRound(),
                        "Result: " + game.getResult(),
                        "White: " + game.getWhitePlayer().getName(),
                        "Black: " + game.getBlackPlayer().getName(),
                        "Eco: " + game.getEco(),
                        "Opening: " + game.getOpening(),
                        "Variation: " + game.getVariation(),
                        "Plycount: " + game.getPlyCount(),
                        "WhiteElo: " + game.getWhitePlayer().getRating(),
                        "BlackElo: " + game.getBlackPlayer().getRating()
                        ]
    }
    for _ in range(0, data.get("Move Number").__len__() - data.get("Meta Data").__len__()):
        data.get("Meta Data").append("-")
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(filePath, index=False)

def importGameFromExcel(file):
    moveCount = 0
    dataFrame = pd.read_excel(file)
    moves = []
    for index, row in dataFrame.iterrows():
        moveCount += 1
        event = dataFrame["Meta Data"][0].split(": ")[1]
        site = dataFrame["Meta Data"][1].split(": ")[1]
        date = dataFrame["Meta Data"][2].split(": ")[1]
        round = dataFrame["Meta Data"][3].split(": ")[1]
        result = dataFrame["Meta Data"][4].split(": ")[1]
        eco = dataFrame["Meta Data"][7].split(": ")[1]
        opening = dataFrame["Meta Data"][8].split(": ")[1]
        plycount = dataFrame["Meta Data"][10].split(": ")[1]
        whitePlayer = Chess.ChessPlayer(
            dataFrame["Meta Data"][5], dataFrame["Meta Data"][11])
        blackPlayer = Chess.ChessPlayer(
            dataFrame["Meta Data"][6], dataFrame["Meta Data"][12])
        variation = dataFrame["Meta Data"][9].split(": ")[1]
        if moveCount % 2 == 0:
            move = Chess.ChessMove(row["Move Number"], Chess.ChessPlayer(
                dataFrame["Meta Data"][5], dataFrame["Meta Data"][10]), row["Move"])
        else:
            move = Chess.ChessMove(row["Move Number"], Chess.ChessPlayer(
                dataFrame["Meta Data"][6], dataFrame["Meta Data"][11]), row["Move"])
        moves.append(move)
    return Chess.ChessGame(event, site, date, round, result, eco, opening, plycount, whitePlayer, blackPlayer, moves, variation)
