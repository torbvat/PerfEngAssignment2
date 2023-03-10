# import ExcelHandler
import DatabaseHandler
from Tree import Printer
import WordHandler

gameReader = DatabaseHandler.DatabaseHandler(
    "Datafiles\Stockfish_15_64-bit.commented.[2600].pgn")
games = gameReader.readGames()


# Excel:
# game_exporter = ExcelHandler.ExcelHandler()
# game_exporter.exportGameToExcel(games[0], "Datafiles\game_0.xlsx")
# imported_game = game_exporter.import_game_from_excel("Datafiles\game_2000.xlsx")

# Word:
wordHandler = WordHandler.WordHandler("testFil.docx", games)
wordHandler.createGraphs()
wordHandler.createDocument()

# Tree:
printer = Printer()
graph = printer.createGraph(games)
printer.drawGamesWithOpening(
    "Datafiles\FrenchOpening.dot", "French", games, 5, 3)
printer.drawGraph(graph, "Datafiles\ChessTree.dot", 5, 3)
printer.drawGamesWithOpening(
    "Datafiles\SicilianOpening.dot", "Sicilian", games, 5, 3)
