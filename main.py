import PgnReader
#import sys
#print(sys.path)
#print(sys.executable)
reader = PgnReader.PgnReader("Stockfish_15_64-bit.commented.[2600].pgn")
#reader = PgnReader.PgnReader("testDatabase.pgn")

print(reader.read_games())