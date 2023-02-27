import Game #Class for storing game data
import Player #Class for storing player data
import ChessMove #Class for storing data about a single move
import re
class DatabaseHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_games(self):
        
        games = []
        with open(self.file_path, 'r') as file:
            game_count = 0
            game_data = file.readline()
            game_data = re.sub(r'\d+\.\s', '\n\\g<0>', game_data) # Split moves into separate lines
            event = site = date = round = result = None
            white_name = white_elo = black_name = black_elo = None
            moves = []
            for line in file:
                if line is None:
                    continue
                elif line.startswith('[Event'):
                    #Får det (forhåpentligvis) til å starte på nytt Game-objekt når den kommer til en ny linje som starter med [Event
                    if game_count:
                        white_player = Player.Player(white_name, white_elo)
                        black_player = Player.Player(black_name, black_elo)
                        games.append(Game.Game(event, site, date, round, result, white_player, black_player, moves))
                        #Legger ikke til første parti fra filen
                        #print(Game.Game(event, site, date, round, result, white_player, black_player, moves))
                        #Moves blir ikke lagt til
                        #print(moves)
                    game_count += 1
                    event = line.split('"')[1]
                    moves = []
                elif line.startswith('[Site '):
                    site = line.split('"')[1]
                elif line.startswith('[Date '):
                    date = line.split('"')[1]
                elif line.startswith('[Round '):
                    round = line.split('"')[1]
                elif line.startswith('[Result '):
                    result = line.split('"')[1]
                elif line.startswith('[White '):
                    white_name = line.split('"')[1]
                elif line.startswith('[Black '):
                    black_name = line.split('"')[1]
                elif line.startswith('[WhiteElo '):
                    white_elo = line.split('"')[1]
                elif line.startswith('[BlackElo '):
                    black_elo = line.split('"')[1]
                elif line.startswith(str(re.match(r'\d+\.', line))) and line is not None:
                    pattern = r"\s+(?=[^{}]*(?:\{|$))"
                    line_elements = re.split(pattern, line)
                    move_number = line_elements[0]
                    move_str_white = line_elements[1]
                    move_comment_white = line_elements[2]
                    move_str_black = line_elements[3]
                    move_comment_black = line_elements[4]
                    moves.append(ChessMove.ChessMove(move_number, white_player, move_str_white, move_comment_white))
                    moves.append(ChessMove.ChessMove(move_number, black_player, move_str_black, move_comment_black)) 
                    #print(moves)
            white_player = Player.Player(white_name, white_elo)
            black_player = Player.Player(black_name, black_elo)
            games.append(Game.Game(event, site, date, round, result, white_player, black_player, moves))
        return games
    
"""
    def importChessDataBase(self, filePath):
        input_file = open(filePath, "r")
        count = self.readDatabase(input_file)
        input_file.close()

    def readLine(self, input_file):
        line = input_file.readline()
        if line=="":
            return None
        return line.rstrip()
    
    def readDatabase(self, input_file):
        step = 1
        line = self.readLine(input_file)
        while True:
            if step==1: # Read a game
                if line==None:
                    break
                else:
                    step = 2
            elif step==2: # Read meta-data
                if re.match("\[", line):
                    match = re.search("\[([a-zA-Z]+)", line)
                    if match:
                        key = match.group(1)

                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        value = match.group(1)
                    print(key + " " + value)
                    line = self.readLine(input_file)
                    if line==None:
                        break
                else:
                    step = 3
            elif step==3: # read moves
                line = self.readLine(input_file)
                if line==None:
                    break
                elif re.match("\[", line):
                    step = 2
""" 
"""
    def read_games(self):
        games = []
        with open(self.file_path, 'r') as file:
            while True:
                game = chess.pgn.read_game(file)
                if game is None:
                    break
                moves = []
                node = game                
                white_player = Player.Player(game.headers["White"], game.headers["WhiteElo"])
                black_player = Player.Player(game.headers["Black"], game.headers["BlackElo"])
                while not node.is_end():
                    next_node = node.variation(0)
                    move_number = node.board().fullmove_number
                    move_text = node.board().san(next_node.move)
                    if node.board().turn == chess.WHITE:
                        moves.append(ChessMove.ChessMove(move_number, white_player, move_text))
                    else:
                        moves.append(ChessMove.ChessMove(move_number, black_player, move_text))
                    node = next_node

                result = game.headers["Result"]
                games.append(Game.Game(game.headers["Event"], game.headers["Site"], game.headers["Date"],
                                       game.headers["Round"], result, white_player, black_player, moves))
        return games
"""