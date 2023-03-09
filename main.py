import ExcelHandler
import DatabaseHandler
from Tree import Printer, Graph
import WordHandler

# reader = DatabaseHandler.DatabaseHandler(
#     "Stockfish_15_64-bit.commented.[2600].pgn")

# print(reader.read_games())

# Excel:
game_reader = DatabaseHandler.DatabaseHandler(
    "Stockfish_15_64-bit.commented.[2600].pgn")
games = game_reader.read_games()
#game_reader.write_to_file(games, "Datafiles\Stockfish_complete_rewritten.pgn")
# print(games[2000].get_variation())
# print(games[0].moves)

# Excel:
#game_exporter = ExcelHandler.ExcelHandler()
#game_exporter.export_game_to_excel(games[0], "Datafiles\game_0.xlsx")
#imported_game = game_exporter.import_game_from_excel("Datafiles\game_2000.xlsx")

# Word:
word_exporter = WordHandler.WordHandler("testFil.docx", games)
# for game in word_exporter.get_games():
#     print(game)
word_exporter.create_graphs()
word_exporter.create_document()

# Tree:
printer = Printer()
graph = printer.createGraph(games)
# print(graph.nodes)
printer.drawGamesWithOpening(
    "Datafiles\FrenchOpening.dot", "French", games, 5, 3)
printer.drawGraph(graph, "Datafiles\ChessTree.dot", 5, 3)
