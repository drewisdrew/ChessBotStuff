# chessbld.py
import chess
import chess.engine
import random
import os

board = chess.Board()
try:
    if "nt" in os.name:
        engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\andre\\Downloads\\stockfish-windows-arm64-universal\\stockfish\\stockfish-windows-arm64-universal.exe")
    elif "posix" in os.name:
        engine = chess.engine.SimpleEngine.popen_uci("/home/drew/Downloads/stockfish/stockfish-linux-x86-64-universal")
    else:
        print("Unexpected OS.")
except FileNotFoundError:
    print("Make sure the engine in in the directory.")
    print("You can change the directory on lines 11/13 depending on your OS.")

moves = 0
blind = False

def move():
    global moves, blind
    moves += 1
    if not blind:
        print(board)

    while not board.is_game_over():
        move = input("Move (SAN): ")
        try:
            board.parse_san(move)
            board.push_san(move)
            break
        except ValueError:
            if move == "peek":
                print(board)
                print("Here is the state of the board.")
            elif move == "blind":
                blind = not blind
                print("Blind:", blind)
            else:
                print("Invalid.")

        
while True:
    white = input("Play as white? Y/N: ")
    if white.lower().strip() == "y":
        white = True
        break
    elif white.lower().strip() == "n":
        white = False
        break
    else:
        print("Invalid.")

if white:
    move()


while not board.is_game_over():
    os.system("clear")
    print("CHESSBLD")
    print("You are playinng as white") if white else print("You are playing as black.")

    result = engine.play(board, chess.engine.Limit(time=0.0001, depth=0))
    print("Engine plays:", board.san(result.move))
    board.push(result.move)

    move()

print(board)
print("END:", board.outcome().termination)
print("WINNER:", board.outcome().winner)
print("MOVES:", moves)
print("GAME OVER!")

engine.quit()