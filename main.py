import ExcelHandler
import DatabaseHandler

reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")

print(reader.read_games())


#Excel:
#game_reader = DatabaseHandler.DatabaseHandler("StockfishShort.pgn")
#games = game_reader.read_games()
#game_exporter_1 = ExcelHandler.ExcelHandler("first_game1.xlsx")
#game_exporter_1.export_game_to_excel(games[0])
