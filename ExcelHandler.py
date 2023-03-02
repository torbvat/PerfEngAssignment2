import pandas as pd
import Game
import ChessMove
import Player
import PgnReader

class ExcelHandler:

    def export_game_to_excel(self, game, file_path):
        data = {
            "Move Number": [move.move_number for move in game.get_moves()],
            "Player Name": [move.player.get_name() for move in game.get_moves()],
            "Player Rating": [move.player.rating for move in game.get_moves()],
            "Move": [move.move_text for move in game.get_moves()],
            "Meta Data": ["Event: " + game.get_event(), 
                          "Site: " + game.get_site(), 
                          "Date: " + game.get_date(), 
                          "Round: " + game.get_round(), 
                          "Result: " + game.get_result(), 
                          "Eco: " + game.get_eco(), 
                          "Opening: " + game.get_opening(), 
                          "Plycount: " + game.get_plycount(), 
                          "White: " + game.get_white_player().get_name(), 
                          "Black: " + game.get_black_player().get_name(), 
                          "Variation: " + game.get_variation()
                        ]
                }
        for _ in range(0, data.get("Move Number").__len__() - data.get("Meta Data").__len__()):
            data.get("Meta Data").append("-")       
        data_frame = pd.DataFrame(data)
        data_frame.to_excel(file_path, index=False)

    def import_game_from_excel(self, file):
        data_frame = pd.read_excel(file)
        moves = []
        for index, row in data_frame.iterrows():
            move = ChessMove.ChessMove(row["Move Number"], Player.Player(row["Player Name"], row["Player Rating"]), row["Move"])
            moves.append(move)
            event = data_frame["Meta Data"][0].split(": ")[1]
            site = data_frame["Meta Data"][1].split(": ")[1]
            date = data_frame["Meta Data"][2].split(": ")[1]
            round = data_frame["Meta Data"][3].split(": ")[1]
            result = data_frame["Meta Data"][4].split(": ")[1]
            eco = data_frame["Meta Data"][5].split(": ")[1]
            opening = data_frame["Meta Data"][6].split(": ")[1]
            plycount = data_frame["Meta Data"][7].split(": ")[1]
            white_player = Player.Player(data_frame["Meta Data"][8].split(": ")[1], 0)
            black_player = Player.Player(data_frame["Meta Data"][9].split(": ")[1], 0)
            variation = data_frame["Meta Data"][10].split(": ")[1]
        return Game.Game(event, site, date, round, result, eco, opening, plycount, white_player, black_player, moves, variation)