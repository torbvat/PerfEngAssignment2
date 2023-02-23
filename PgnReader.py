import chess.pgn
import Game
import Player
import ChessMove
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
                while not game.is_end():
                    next_node = game.variation(0)
                    move_number = game.board().fullmove_number
                    white_player = Player.Player(game.headers["White"], game.headers["WhiteElo"])
                    black_player = Player.Player(game.headers["Black"], game.headers["BlackElo"])
                    move_text = game.board().san(next_node.move)
                    if move_number % 2 == 0:
                        moves.append(ChessMove.ChessMove(move_number, black_player, move_text))
                    else:
                        moves.append(ChessMove.ChessMove(move_number, white_player, move_text))
                    game = next_node
                result = game.headers["Result"]
                games.append(Game.Game(game.headers["Event"], game.headers["Site"], game.headers["Date"],
                                       game.headers["Round"], result, white_player, black_player, moves))
        return games