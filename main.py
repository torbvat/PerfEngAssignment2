import ExcelHandler
import DatabaseHandler

#Database:
reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
game_reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
games = game_reader.read_games()
first_two_games = game_reader.read_games(2)
#Excel:
game_exporter = ExcelHandler.ExcelHandler()
game_exporter.export_game_to_excel(games[0], "first_game.xlsx")
imported_game = game_exporter.import_game_from_excel("first_game.xlsx")
game_reader.write_to_file([imported_game], "imported_game_from_excel.pgn")
game_reader.write_to_file(games, "StockfishShort_rewritten.pgn")
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


