from docx import Document
import matplotlib.pyplot as plt
import statistics


class WordHandler:
    def __init__(self, filePath, games):
        self.filePath = filePath
        self.games = games
        self.medianOfAllGames = 0
        self.SDofAllGames = 0
        self.medianOfWhiteGames = 0
        self.SDofWhiteGames = 0
        self.medianOfBlackGames = 0
        self.SDofBlackGames = 0

    def getGames(self):
        return self.games

    def isWhiteGame(self, game):
        return game.whitePlayer.getName().startswith("Stockfish")

    def isBlackGame(self, game):
        return game.blackPlayer.getName().startswith("Stockfish")

    def isStockfishWin(self, game):
        return (self.isWhiteGame(game) and game.result == "1-0") or (self.isBlackGame(game) and game.result == "0-1")

    def isStockfishLoss(self, game):
        return (self.isWhiteGame(game) and game.result == "0-1") or (self.isBlackGame(game) and game.result == "1-0")

    def createDocument(self):
        document = Document()

        document.add_heading('Chess game', 0)
        self.addResultTables(document)
        self.addMedianSDTables(document)
        document.add_picture('proportionResultsPlot.png')
        document.add_picture('proportionStockfishPlot.png')
        document.save("testFil.docx")

    def addResultTables(self, document):

        # Calculate games won:
        whiteWon = 0
        whiteDrawn = 0
        whiteLost = 0
        blackWon = 0
        blackDrawn = 0
        blackLost = 0

        for game in self.games:
            if game.whitePlayer.getName().startswith("Stockfish"):
                if game.result == "1-0":
                    whiteWon += 1
                elif game.result == "0-1":
                    whiteLost += 1
                elif game.result == "1/2-1/2":
                    whiteDrawn += 1
            elif game.blackPlayer.getName().startswith("Stockfish"):
                if game.result == "0-1":
                    blackWon += 1
                elif game.result == "1-0":
                    blackLost += 1
                elif game.result == "1/2-1/2":
                    blackDrawn += 1

        gamesWon = whiteWon + blackWon
        gamesDrawn = whiteDrawn + blackDrawn
        gamesLost = whiteLost + blackLost

        # Create tables
        document.add_heading("Stockfish all games", 3)
        allGamesTable = document.add_table(rows=2, cols=3)
        allGamesTable.style = "Medium Shading 1"
        header_row = allGamesTable.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = allGamesTable.rows[1].cells
        value_row[0].text = str(gamesWon)
        value_row[1].text = str(gamesDrawn)
        value_row[2].text = str(gamesLost)

        document.add_heading("Stockfish white games", 3)
        whiteGamesTable = document.add_table(rows=2, cols=3)
        whiteGamesTable.style = "Medium Shading 1"
        header_row = whiteGamesTable.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = whiteGamesTable.rows[1].cells
        value_row[0].text = str(whiteWon)
        value_row[1].text = str(whiteDrawn)
        value_row[2].text = str(whiteLost)

        document.add_heading("Stockfish black games", 3)
        blackGamesTable = document.add_table(rows=2, cols=3)
        blackGamesTable.style = "Medium Shading 1"
        header_row = blackGamesTable.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = blackGamesTable.rows[1].cells
        value_row[0].text = str(blackWon)
        value_row[1].text = str(blackDrawn)
        value_row[2].text = str(blackLost)

    def addMedianSDTables(self, document):
        document.add_heading(
            "Median and standard deviation for length of games", 3)
        medianSDTable = document.add_table(rows=1, cols=2)
        medianSDTable.style = "Medium Shading 1"
        tableHeader = medianSDTable.rows[0].cells
        tableHeader[0].text = "Type"
        tableHeader[1].text = "Value"

        records = (
            ("Median all games", self.medianOfAllGames),
            ("SD all games", self.SDofAllGames),
            ("Median white games", self.medianOfWhiteGames),
            ("SD white games", self.SDofWhiteGames),
            ("Median black games", self.medianOfBlackGames),
            ("SD black games", self.SDofBlackGames)
        )

        for type, value in records:
            row_cells = medianSDTable.add_row().cells
            row_cells[0].text = type
            row_cells[1].text = str(round(value, 2))

    def createResultGraph(self):
        longestGameCount = int(self.games[0].plycount)
        longestWhiteGameCount = 0
        longestBlackGameCount = 0
        movesAllGames = []
        movesWhiteGames = []
        movesBlackGames = []
        gamesStockfishWhite = []
        gamesStockfishBlack = []

        for game in self.games:
            # Find stockfish white and black games
            if self.isWhiteGame(game):
                gamesStockfishWhite.append(game)
                movesWhiteGames.append(int(game.plycount))
                if int(game.plycount) > longestWhiteGameCount:
                    longestWhiteGameCount = int(game.plycount)
            elif self.isBlackGame(game):
                gamesStockfishBlack.append(game)
                movesBlackGames.append(int(game.plycount))
                if int(game.plycount) > longestBlackGameCount:
                    longestBlackGameCount = int(game.plycount)

            # Find longest game
            movesAllGames.append(int(game.plycount))
            if int(game.plycount) > longestGameCount:
                longestGameCount = int(game.plycount)

        nrOfGames = len(self.games)
        nrOfWhiteGames = len(gamesStockfishWhite)
        nrOfBlackGames = len(gamesStockfishBlack)

        # Find median and SD of all games, stockfish games with white and stockfish games with black
        self.medianOfAllGames = statistics.median(movesAllGames)
        self.SDofAllGames = statistics.pstdev(movesAllGames)
        if movesWhiteGames:
            self.medianOfWhiteGames = statistics.median(movesWhiteGames)
            self.SDofWhiteGames = statistics.pstdev(movesWhiteGames)
        if movesBlackGames:
            self.medianOfBlackGames = statistics.median(movesBlackGames)
            self.SDofBlackGames = statistics.pstdev(movesBlackGames)

        moveList = list(range(1, int(longestGameCount) + 2))
        whiteMoveList = list(range(1, int(longestWhiteGameCount) + 2))
        blackMoveList = list(range(1, int(longestBlackGameCount) + 2))
        ongoingGamesOnMove = [0] * (int(longestGameCount) + 1)
        ongoingWhiteGamesOnMove = [0] * (int(longestWhiteGameCount) + 1)
        ongoingBlackGamesOnMove = [0] * (int(longestBlackGameCount) + 1)
        for game in self.games:
            gameLength = int(game.plycount)
            if self.isWhiteGame(game):
                for i in range(gameLength):
                    ongoingWhiteGamesOnMove[i] += 1
            elif self.isBlackGame(game):
                for i in range(gameLength):
                    ongoingBlackGamesOnMove[i] += 1
            for i in range(gameLength):
                ongoingGamesOnMove[i] += 1

        proportionOfGames = []
        proportionOfWhiteGames = []
        proportionOfBlackGames = []
        for i in range(len(ongoingGamesOnMove)):
            proportionOfGames.append(
                round(ongoingGamesOnMove[i]*100/nrOfGames, 2))

        for i in range(len(ongoingWhiteGamesOnMove)):
            proportionOfWhiteGames.append(
                round(ongoingWhiteGamesOnMove[i]*100/nrOfWhiteGames, 2))

        for i in range(len(ongoingBlackGamesOnMove)):
            proportionOfBlackGames.append(
                round(ongoingBlackGamesOnMove[i]*100/nrOfBlackGames, 2))

        plt.figure(1)
        plt.plot(moveList, proportionOfGames, 'b', label="All games")
        plt.plot(whiteMoveList, proportionOfWhiteGames,
                 'r', label="White games")
        plt.plot(blackMoveList, proportionOfBlackGames,
                 'g', label="Black games")
        plt.xlim(0, longestGameCount+2)
        plt.ylim(0, 102)
        plt.xlabel("Number of moves")
        plt.ylabel("Percentage of games ongoing")
        plt.suptitle("Proportion of games still ongoing after n moves")
        plt.legend(loc="upper right")
        plt.savefig("proportionResultsPlot.png")

    def createSFResultGraph(self):
        longestGameCount = int(self.games[0].plycount)
        wonGames = []
        lostGames = []
        longestWonGameCount = 0
        longestLostGameCount = 0

        for game in self.games:
            if self.isStockfishWin(game):
                wonGames.append(game)
                if int(game.plycount) > longestWonGameCount:
                    longestWonGameCount = int(game.plycount)
            elif self.isStockfishLoss(game):
                lostGames.append(game)
                if int(game.plycount) > longestLostGameCount:
                    longestLostGameCount = int(game.plycount)

        longestGameCount = max(longestWonGameCount, longestLostGameCount)
        nrOfWonGames = len(wonGames)
        nrOfLostGames = len(lostGames)

        # if wonGames:
        #     self.medianOfWonGames = statistics.median(wonGames)
        #     self.SDofWonGames = statistics.pstdev(wonGames)
        # if lostGames:
        #     self.medianOfLostGames = statistics.median(lostGames)
        #     self.SDofLostGames = statistics.pstdev(lostGames)

        wonMoveList = list(range(1, int(longestWonGameCount) + 2))
        lostMoveList = list(range(1, int(longestLostGameCount) + 2))

        ongoingWonGamesOnMove = [0] * (int(longestWonGameCount) + 1)
        ongoingLostGamesOnMove = [0] * (int(longestLostGameCount) + 1)

        for game in self.games:
            gameLength = int(game.plycount)
            if self.isStockfishWin(game):
                for i in range(gameLength):
                    ongoingWonGamesOnMove[i] += 1
            elif self.isStockfishLoss(game):
                for i in range(gameLength):
                    ongoingLostGamesOnMove[i] += 1

        proportionOfWonGames = []
        proportionOfLostGames = []

        for i in range(len(ongoingWonGamesOnMove)):
            proportionOfWonGames.append(
                round(ongoingWonGamesOnMove[i]*100/nrOfWonGames))

        for i in range(len(ongoingLostGamesOnMove)):
            proportionOfLostGames.append(
                round(ongoingLostGamesOnMove[i]*100/nrOfLostGames))

        plt.figure(2)
        plt.plot(wonMoveList, proportionOfWonGames, 'g', label="Games won")
        plt.plot(lostMoveList, proportionOfLostGames, 'r', label="Games lost")
        plt.xlim(0, longestGameCount+2)
        plt.ylim(0, 102)
        plt.xlabel("Number of moves")
        plt.ylabel("Percentage of games ongoing")
        plt.suptitle(
            "Proportion of Stockfish games still ongoing after n moves")
        plt.legend(loc="upper right")
        plt.savefig("proportionStockfishPlot.png")

    def createGraphs(self):
        self.createResultGraph()
        self.createSFResultGraph()
