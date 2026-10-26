# chessbld.py
import chess
import chess.engine
import random
import os

print("CHESSBLD")
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\andre\\Downloads\\stockfish-windows-arm64-universal\\stockfish\\stockfish-windows-arm64-universal.exe")
moves = 0


if random.randint(2, 2) == 1:
    print("You start as white.")
    moves += 1
    while True:
        move = input("Move (SAN):")
        try:
            board.parse_san(move)   
            board.push_san(move)
            break
        except ValueError:
            if move == "peek":
                print(board)
                print("Here is the state of the board.")
            else:
                print("Invalid.")
else:
    print("You start as black.")

while not board.is_game_over():
    os.system("cls")
    
    print("CHESSBLD")
    result = engine.play(board, chess.engine.Limit(time=0.0001, depth=0))
    print("Engine plays:", board.san(result.move))
    board.push(result.move)

    moves += 1
    print(board)
    while True:
        move = input("Move (SAN): ")
        try:
            board.parse_san(move)
            board.push_san(move)
            break
        except ValueError:
            if move == "peek":
                print(board)
                print("Here is the state of the board.")
            else:
                print("Invalid.")
    

    
print("END:", board.outcome().termination)
print("WINNER:", board.outcome().winner)
print("MOVES:", moves)

engine.quit()