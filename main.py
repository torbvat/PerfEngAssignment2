import ExcelHandler
import DatabaseHandler

reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
#Excel:
game_reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
games = game_reader.read_games()
first_two_games = game_reader.read_games(2)

#print(games)
#print(first_two_games)
#print(games[0].moves)
game_exporter = ExcelHandler.ExcelHandler()
game_exporter.export_game_to_excel(games[0], "first_game.xlsx")
imported_game = game_exporter.import_game_from_excel("first_game.xlsx")
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

#game_exporter_2 = ExcelHandler.ExcelHandler("second_game.xlsx")
#print(games[0].moves)
#game_exporter_2.export_game_to_excel(games[1])

#game_reader.write_to_file(games, "testfile2.pgn")
