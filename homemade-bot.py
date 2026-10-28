# homemade-bot.py
# not related to chessbld.py
# my first attempt at a chess bot
import chess
import os

# per square tables
#region psts

pst_pawn = [
0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50, 
10, 10, 20, 30, 30, 20, 10, 10,
5,  5, 10, 25, 25, 10,  5,  5,
0,  0,  0, 20, 20,  0,  0,  0,
5, -5,-10,  0,  0,-10, -5,  5,
5, 10, 10,-20,-20, 10, 10,  5,
0,  0,  0,  0,  0,  0,  0,  0
]

pst_knight = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50
]

pst_bishop = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20
]

pst_rook = [
0,  0,  0,  0,  0,  0,  0,  0,
5, 10, 10, 10, 10, 10, 10,  5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
0,  0,  0,  5,  5,  0,  0,  0
]

pst_queen = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
-5,  0,  5,  5,  5,  5,  0, -5,
0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]

pst_king = [
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
20, 20,  0,  0,  0,  0, 20, 20,
20, 30, 10,  0,  0, 10, 30, 20
]

pst_king_endgame = [
-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50
]

#endregion psts

board = chess.Board()

# Evaluate how good the position is (to play the good move good one)
piece_values = {
    chess.QUEEN: 900,
    chess.ROOK: 500,
    chess.BISHOP: 330,
    chess.KNIGHT: 300,
    chess.PAWN: 100,
}

def evaluate(white1):
    """Material score from the perspective of white1 (True = white, False = black)."""
    score = 0
    for piece in board.piece_map().values():
        value = piece_values.get(piece.piece_type, 0)  # kings = 0
        score += value if piece.color == white1 else -value
    return score



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
    print("CHESS but the bot is STUPID")
    print("You are playinng as white.") if white else print("You are playing as black.")
    evals = []
    for i in list(board.legal_moves):
        board.push(i)
        evals.append(evaluate(True) if not white else evaluate(False))
        board.pop()

    bestmove = evals.index(max(evals))
    result = (list(board.legal_moves)[bestmove])    
    print(bestmove)
    print(result)
    print(evals)
    print("\n")
    print(list(board.legal_moves))



    print("Engine plays:", board.san(result))
    board.push(result)

    move()