import ExcelHandler
import DatabaseHandler

#Database:
game_reader = DatabaseHandler.DatabaseHandler("Stockfish_15_64-bit.commented.[2600].pgn")
games = game_reader.read_games()
game_reader.write_to_file(games, "Stockfish_complete_rewritten.pgn")
print(games[2000].get_variation())

#Excel:
game_exporter = ExcelHandler.ExcelHandler()
game_exporter.export_game_to_excel(games[2000], "game_2000_v2.xlsx")
imported_game = game_exporter.import_game_from_excel("game_2000_v2.xlsx")

game_reader.write_to_file(([imported_game]), "game_2000_v2.pgn")


"""
print(imported_game.black_player)
print(imported_game.white_player)
print(imported_game.moves)
print(imported_game.event)
print(imported_game.site)
print(imported_game.date)
print(imported_game.round)
print(imported_game.result)
print(imported_game.eco)
print(imported_game.opening)
print(imported_game.plycount)
print(imported_game.variation)
"""


