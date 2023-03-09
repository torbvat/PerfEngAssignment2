import ExcelHandler
import DatabaseHandler
import WordHandler

# reader = DatabaseHandler.DatabaseHandler(
#     "Stockfish_15_64-bit.commented.[2600].pgn")

# print(reader.read_games())

# Excel:
game_reader = DatabaseHandler.DatabaseHandler(
    "Stockfish_15_64-bit.commented.[2600].pgn")
games = game_reader.read_games()
# game_exporter = ExcelHandler.ExcelHandler("first_game.xlsx")
# # print(games[0].moves)
# game_exporter.export_game_to_excel(games[0])

# game_exporter_2 = ExcelHandler.ExcelHandler("second_game.xlsx")
# print(games[0].moves)
# game_exporter_2.export_game_to_excel(games[1])

# Word:
word_exporter = WordHandler.WordHandler("testFil.docx", games)
# for game in word_exporter.get_games():
#     print(game)
word_exporter.create_graphs()
word_exporter.create_document()
