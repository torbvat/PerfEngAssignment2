import ExcelHandler
import DatabaseHandler

reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")

print(reader.read_games())

#Excel:
game_reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
games = game_reader.read_games()
game_exporter = ExcelHandler.ExcelHandler("first_game.xlsx")
#print(games[0].moves)
game_exporter.export_game_to_excel(games[0])

game_exporter_2 = ExcelHandler.ExcelHandler("second_game.xlsx")
print(games[0].moves)
game_exporter_2.export_game_to_excel(games[1])
