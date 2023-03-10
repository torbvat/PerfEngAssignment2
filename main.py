import ExcelHandler
import DatabaseHandler
from Tree import Printer
import WordHandler
import pydot



gameReader = DatabaseHandler.DatabaseHandler(
    "Datafiles\Stockfish_15_64-bit.commented.[2600].pgn")
games = gameReader.readGames()


# Excel:
game_exporter = ExcelHandler.ExcelHandler()
game_exporter.exportGameToExcel(games[0], "Datafiles\game1.xlsx")
# imported_game = game_exporter.import_game_from_excel("Datafiles\game_2000.xlsx")


# Tree:
printer = Printer()
graph = printer.createGraph(games)
printer.drawGamesWithOpening(
    "Datafiles\FrenchOpening.dot", "French", games, 5, 3)
printer.drawGraph(graph, "Datafiles\ChessTree.dot", 5, 3)
printer.drawGamesWithOpening(
    "Datafiles\SicilianOpening.dot", "Sicilian", games, 5, 3)

(graph,) = pydot.graph_from_dot_file('Datafiles\FrenchOpening.dot')
graph.write_png('Datafiles\FrenchOpening.png')

(graph2,) = pydot.graph_from_dot_file('Datafiles\SicilianOpening.dot')
graph2.write_png('Datafiles\SicilianOpening.png')



# Word:
wordHandler = WordHandler.WordHandler("testFil2.docx", games)
wordHandler.createGraphs()
wordHandler.createDocument(["Datafiles\FrenchOpening.png", "Datafiles\SicilianOpening.png" ])
