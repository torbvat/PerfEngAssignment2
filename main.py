import ExcelHandler
import DatabaseHandler
from Tree import Printer, Graph

# Database:
# game_reader = DatabaseHandler.DatabaseHandler(
#     "Datafiles\StockfishShort.pgn")
game_reader = DatabaseHandler.DatabaseHandler(
    "Datafiles\Stockfish_15_64-bit.commented.[2600].pgn")
games = game_reader.read_games()
#game_reader.write_to_file(games, "Datafiles\Stockfish_complete_rewritten.pgn")
# print(games[2000].get_variation())
# print(games[0].moves)

# Excel:
#game_exporter = ExcelHandler.ExcelHandler()
#game_exporter.export_game_to_excel(games[0], "Datafiles\game_0.xlsx")
#imported_game = game_exporter.import_game_from_excel("Datafiles\game_2000.xlsx")

#game_reader.write_to_file(([imported_game]), "Datafiles\game_0.pgn")
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

# Tree:
printer = Printer(games)
graph = printer.createGraph(3)
print(graph.nodes)
# Finn ut koffor dybda ikkje blir større når vi øke parameterennnnnnnnn
printer.drawDiagram(graph, "MyNet2.dot")
