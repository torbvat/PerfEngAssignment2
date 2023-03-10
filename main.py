import ExcelHandler
import DatabaseHandler
from Tree import Printer
import WordHandler
import pydot


#Extract games from database
gameReader = DatabaseHandler.DatabaseHandler(
    "Datafiles\Stockfish_15_64-bit.commented.[2600].pgn")
games = gameReader.readGames() #list of all games in database
#------------------------------------------------------------



#Exports first game from database to excel:
firstGame = games[0]
ExcelHandler.exportGameToExcel(firstGame, "Datafiles\game_0.xlsx")
# Creates a game instance from the excel file:
importedGame = ExcelHandler.importGameFromExcel("Datafiles\game_0.xlsx")
print(importedGame)
#------------------------------------------------------------


# Tree:
printer = Printer()
#Creates a tree from all games in database:
graph = printer.createTree(games, "Datafiles\AllGames.dot", 5, 3)

#Creates a tree from all games with the French opening:
french = printer.createTreeWithOpening("Datafiles\FrenchOpening.dot", "French", games, 5, 3)
#Creates a tree from all games with the Sicilian opening:
sicilian = printer.createTreeWithOpening("Datafiles\SicilianOpening.dot", "Sicilian", games, 5, 3)

#Converts the .dot files to .png files:
(graph,) = pydot.graph_from_dot_file(french)
FrenchGraph = graph.write_png('Datafiles\FrenchOpening.png')

(graph2,) = pydot.graph_from_dot_file(sicilian)
SicilianGraph = graph2.write_png('Datafiles\SicilianOpening.png')
#------------------------------------------------------------


# Word:
wordHandler = WordHandler.WordHandler("Datafiles\Report.docx", games)
wordHandler.createGraphs()
wordHandler.createDocument(["Datafiles\FrenchOpening.png", "Datafiles\SicilianOpening.png"], ["French", "Sicilian"], 10)
