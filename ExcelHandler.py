import pandas as pd
import Chess #Chess.py is a file that contains the classes for the chess game

class ExcelHandler:

    def export_game_to_excel(self, game, file_path):
        data = {
            "Move Number": [move.getMoveNumber() for move in game.getMoves()],
            "Move": [move.getMoveText for move in game.getMoves()],
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
        data_frame = pd.DataFrame(data)
        data_frame.to_excel(file_path, index=False)

    def import_game_from_excel(self, file):
        move_count = 0
        data_frame = pd.read_excel(file)
        moves = []
        for index, row in data_frame.iterrows():
            move_count += 1
            event = data_frame["Meta Data"][0].split(": ")[1]
            site = data_frame["Meta Data"][1].split(": ")[1]
            date = data_frame["Meta Data"][2].split(": ")[1]
            round = data_frame["Meta Data"][3].split(": ")[1]
            result = data_frame["Meta Data"][4].split(": ")[1]
            eco = data_frame["Meta Data"][7].split(": ")[1]
            opening = data_frame["Meta Data"][8].split(": ")[1]
            plycount = data_frame["Meta Data"][10].split(": ")[1]
            white_player = Chess.ChessPlayer(data_frame["Meta Data"][5], data_frame["Meta Data"][11])
            black_player = Chess.ChessPlayer(data_frame["Meta Data"][6], data_frame["Meta Data"][12])
            variation = data_frame["Meta Data"][9].split(": ")[1]
            if move_count % 2 == 0:
                move = Chess.ChessMove(row["Move Number"], Chess.ChessPlayer(data_frame["Meta Data"][5], data_frame["Meta Data"][10]), row["Move"])
            else:
                move = Chess.ChessMove(row["Move Number"], Chess.ChessPlayer(data_frame["Meta Data"][6], data_frame["Meta Data"][11]), row["Move"])
            moves.append(move)            
        return Chess.ChessGame(event, site, date, round, result, eco, opening, plycount, white_player, black_player, moves, variation)