import PgnReader
#import sys
#print(sys.path)
#print(sys.executable)
reader = PgnReader.PgnReader("C:\\Users\\torbj\\OneDrive\\Documentos\\Studie\\VAR_SEMESTER_2023\\Performance engineering\\Assignment_2\\Stockfish_15_64-bit.commented.[2600].pgn")

print(reader.read_games())