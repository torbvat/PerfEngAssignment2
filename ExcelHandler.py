import pandas as pd
import Game
import ChessMove
import Player
import PgnReader
import numpy as np

class ExcelHandler:

    def __init__(self, file_path):
        self.file_path = file_path
    
    def export_game_to_excel(self, game):
        data = {
            "Move Number": [move.move_number for move in game.moves],
            "Player Name": [move.player.name for move in game.moves],
            "Player Elo": [move.player.elo for move in game.moves],
            "Move": [move.move_text for move in game.moves]
        }
        df = pd.DataFrame(data)
        df.to_excel(self.file_path, index=False)

game_reader = PgnReader.PgnReader("Stockfish_15_64-bit.commented.[2600].pgn")
games = game_reader.read_games()

game_exporter = ExcelHandler("firstGame.xlsx")
game_exporter.export_game_to_excel(games[0])