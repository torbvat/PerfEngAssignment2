import chess.pgn
import Game #Class for storing game data
import Player #Class for storing player data
import ChessMove #Class for storing data about a single move
class PgnReader:
    def __init__(self, file_path):
        self.file_path = file_path

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