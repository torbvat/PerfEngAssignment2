import Game #Class for storing game data
import Player #Class for storing player data
import ChessMove #Class for storing data about a single move
import re
class DatabaseHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_games(self):
        games = []
        moves = []
        move_string = ""
        with open(self.file_path, 'r') as file:
            event = site = date = round = result = eco = opening  = plycount = None
            white_name = white_elo = black_name = black_elo = None
            variation = "Standard"
            for line in file:
                if line is None or line=="\n" or line == " " or line == "": #Skip empty lines
                    continue
                elif line.startswith('[Event'):
                    moves = []
                    event = line.split('"')[1]
                elif line.startswith('[Site '):
                    site = line.split('"')[1]
                elif line.startswith('[Date '):
                    date = line.split('"')[1]
                elif line.startswith('[Round '):
                    round = line.split('"')[1]
                elif line.startswith('[White '):
                    white_name = line.split('"')[1]
                elif line.startswith('[Black '):
                    black_name = line.split('"')[1]
                elif line.startswith('[Result '):
                    result = line.split('"')[1]
                elif line.startswith('[ECO '):
                    eco = line.split('"')[1]
                elif line.startswith('[Opening '):
                    opening = line.split('"')[1]
                elif line.startswith('[Variation '):
                    variation = line.split('"')[1]
                elif line.startswith('[PlyCount '):
                    plycount = line.split('"')[1]
                elif line.startswith('[WhiteElo '):
                    white_elo = line.split('"')[1]
                elif line.startswith('[BlackElo '):
                    black_elo = line.split('"')[1]
                else:
                    move_string += line.strip("\n")
                    
                if move_string.endswith("1-0") or move_string.endswith("0-1") or move_string.endswith("1/2-1/2"):
                    white_player = Player.Player(white_name, white_elo)
                    black_player = Player.Player(black_name, black_elo)
                    move_string = move_string.replace(".", " ") #Replace all periods with spaces to seperate moves and move numbers when creating a list
                    move_elements = re.findall(r'\S+', re.sub(r'{.*?}', '', move_string)) #Remove comments and creates a list of all elements in move_string
                    for i in range(0, len(move_elements)-2, 3):
                        if move_elements[i+2] == "1-0" or move_elements[i+2] == "0-1" or move_elements[i+2] == "1/2-1/2":
                            white_move = ChessMove.ChessMove(move_elements[i].strip("."), white_player, move_elements[i+1])
                            moves.append(white_move)
                            break
                        move_number = move_elements[i].strip(".")
                        move_str_white = move_elements[i+1]
                        move_str_black = move_elements[i+2]
                        black_move = ChessMove.ChessMove(move_number, black_player, move_str_black)
                        white_move = ChessMove.ChessMove(move_number, white_player, move_str_white)
                        
                        moves.append(white_move)
                        moves.append(black_move)
                    move_string = ""
                    games.append(Game.Game(event, site, date, round, result, eco, opening, plycount, white_player, black_player, moves, variation))
        return games
    
    def write_to_file(self, Games, file_path):
        with open(file_path, 'w') as file:
            for game in Games:
                move_counter = 0
                file.write("[Event\t" + game.get_event() + "]\n")
                file.write("[Site\t" + game.get_site() + "]\n")
                file.write("[Date\t" + game.get_date() + "]\n")
                file.write("[Round\t" + game.get_round() + "]\n")
                file.write("[White\t" + game.get_white_player().get_name() + "]\n")
                file.write("[Black\t" + game.get_black_player().get_name() + "]\n")
                file.write("[Result\t" + game.get_result() + "]\n")
                file.write("[ECO\t" + game.get_eco() + "]\n")
                file.write("[Opening\t" + game.get_opening() + "]\n")
                file.write("[Variation\t" + game.get_variation() + "]\n")
                file.write("[PlyCount\t" + game.get_plycount() + "]\n")
                file.write("[WhiteElo\t" + game.get_white_player().get_rating() + "]\n")
                file.write("[BlackElo\t" + game.get_black_player().get_rating() + "]\n")
                file.write("\n")
                for i in range(0, len(game.get_moves()), 2):
                    move_counter += 1
                    file.write(game.get_moves()[i].get_move_number() + ". " + game.get_moves()[i].get_move_text() + " " + game.get_moves()[i+1].get_move_text()+ " ")\
                    if i+1 < len(game.get_moves()) else file.write(game.get_moves()[i].get_move_number() + ". " + game.get_moves()[i].get_move_text() + " " + game.get_result() + "\n\n")
                    if move_counter % 4 == 0:
                        file.write("\n")



    
    