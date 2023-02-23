import PgnReader
import ExcelHandler

reader = PgnReader.PgnReader("StockfishShort.pgn")

print(reader.read_games())

#Excel:
game_reader = PgnReader.PgnReader("StockfishShort.pgn")
games = game_reader.read_games()
game_exporter_1 = ExcelHandler.ExcelHandler("first_game.xlsx")
game_exporter_1.export_game_to_excel(games[0])
game_exporter_2 = ExcelHandler.ExcelHandler("second_game.xlsx")
game_exporter_2.export_game_to_excel(games[1])