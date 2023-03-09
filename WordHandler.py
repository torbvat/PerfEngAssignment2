from docx import Document
import matplotlib.pyplot as plt
import statistics


class WordHandler:
    def __init__(self, filepath, games):
        self.filepath = filepath
        self.games = games
        self.medianOfAllGames = 0
        self.SDofAllGames = 0
        self.medianOfWhiteGames = 0
        self.SDofWhiteGames = 0
        self.medianOfBlackGames = 0
        self.SDofBlackGames = 0

    def get_games(self):
        return self.games

    def isWhiteGame(self, game):
        return game.white_player.get_name().startswith("Stockfish")

    def isBlackGame(self, game):
        return game.black_player.get_name().startswith("Stockfish")

    def isStockfishWin(self, game):
        return (self.isWhiteGame(game) and game.result == "1-0") or (self.isBlackGame(game) and game.result == "0-1")

    def isStockfishLoss(self, game):
        return (self.isWhiteGame(game) and game.result == "0-1") or (self.isBlackGame(game) and game.result == "1-0")

    def create_document(self):
        document = Document()

        document.add_heading('Chess game', 0)
        self.add_result_tables(document)
        self.add_medianSD_tables(document)
        document.add_picture('proportionResultsPlot.png')
        document.add_picture('proportionStockfishPlot.png')
        document.save("testFil.docx")

    def add_result_tables(self, document):

        # Calculate games won:
        white_won = 0
        white_drawn = 0
        white_lost = 0
        black_won = 0
        black_drawn = 0
        black_lost = 0

        for game in self.games:
            if game.white_player.get_name().startswith("Stockfish"):
                if game.result == "1-0":
                    white_won += 1
                elif game.result == "0-1":
                    white_lost += 1
                elif game.result == "1/2-1/2":
                    white_drawn += 1
            elif game.black_player.get_name().startswith("Stockfish"):
                if game.result == "0-1":
                    black_won += 1
                elif game.result == "1-0":
                    black_lost += 1
                elif game.result == "1/2-1/2":
                    black_drawn += 1

        games_won = white_won + black_won
        games_drawn = white_drawn + black_drawn
        games_lost = white_lost + black_lost

        # Create tables
        document.add_heading("Stockfish all games", 3)
        all_games_table = document.add_table(rows=2, cols=3)
        all_games_table.style = "Medium Shading 1"
        header_row = all_games_table.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = all_games_table.rows[1].cells
        value_row[0].text = str(games_won)
        value_row[1].text = str(games_drawn)
        value_row[2].text = str(games_lost)

        document.add_heading("Stockfish white games", 3)
        white_games_table = document.add_table(rows=2, cols=3)
        white_games_table.style = "Medium Shading 1"
        header_row = white_games_table.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = white_games_table.rows[1].cells
        value_row[0].text = str(white_won)
        value_row[1].text = str(white_drawn)
        value_row[2].text = str(white_lost)

        document.add_heading("Stockfish black games", 3)
        black_games_table = document.add_table(rows=2, cols=3)
        black_games_table.style = "Medium Shading 1"
        header_row = black_games_table.rows[0].cells
        header_row[0].text = 'Won'
        header_row[1].text = 'Drawn'
        header_row[2].text = 'Lost'
        value_row = black_games_table.rows[1].cells
        value_row[0].text = str(black_won)
        value_row[1].text = str(black_drawn)
        value_row[2].text = str(black_lost)

    def add_medianSD_tables(self, document):
        document.add_heading(
            "Median and standard deviation for length of games", 3)
        medianSD_table = document.add_table(rows=1, cols=2)
        medianSD_table.style = "Medium Shading 1"
        tableHeader = medianSD_table.rows[0].cells
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
            row_cells = medianSD_table.add_row().cells
            row_cells[0].text = type
            row_cells[1].text = str(round(value, 2))

    def create_result_graph(self):
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
        print(nrOfBlackGames)

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
        plt.show()

    def create_SF_result_graph(self):
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
        print(longestGameCount)

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

        print(wonMoveList)
        print(lostMoveList)

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
        plt.show()

    def create_graphs(self):
        self.create_result_graph()
        self.create_SF_result_graph()
