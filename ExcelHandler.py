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
            "Player Rating": [move.player.rating for move in game.moves],
            "Move": [move.move_text for move in game.moves]
        }
        data_frame = pd.DataFrame(data)
        data_frame.to_excel(self.file_path, index=False)