# homemade-bot.py
# not related to chessbld.py
# my first attempt at a chess bot
import chess
import subprocess
import random

# per square tables
#region psts

pst_pawn = [
0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50, 
10, 10, 20, 30, 30, 20, 10, 10,
5,  5, 10, 25, 25, 10,  5,  5,
0,  0,  0, 30, 30,  0,  0,  0,
5, -5,-10,  0,  0,-10, -5,  5,
5, 10, 10,-20,-20, 10, 10,  5,
0,  0,  0,  0,  0,  0,  0,  0
]

pst_knight = [
-50,-30,-30,-30,-30,-30,-30,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-30,-30,-30,-30,-30,-30,-50
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
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # if need nerf

# Evaluate how good the position is (to play the good move good one)
piece_values = {
    chess.QUEEN: 900,
    chess.ROOK: 500,
    chess.BISHOP: 330,
    chess.KNIGHT: 300,
    chess.PAWN: 100,
    chess.KING: 0
}

def evaluate():
    # Material score
    score = 0
    for piece in board.piece_map().values():
        value = piece_values.get(piece.piece_type)
        score += value if piece.color == chess.WHITE else -value

    # TODO: PST incorporation
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    score += pst_pawn[sq ^ 56]
                else:
                    score -= pst_pawn[sq]

            if piece.piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    score += pst_knight[sq ^ 56]
                else:
                    score -= pst_knight[sq]

            if piece.piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    score += pst_bishop[sq ^ 56]
                else:
                    score -= pst_bishop[sq]

            if piece.piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    score += pst_rook[sq ^ 56]
                else:
                    score -= pst_rook[sq]

            if piece.piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    score += pst_queen[sq ^ 56]
                else:
                    score -= pst_queen[sq]

            if piece.piece_type == chess.KING:
                queens = 0
                for sq2 in chess.SQUARES:
                    piece2 = board.piece_at(sq2)
                    if piece2 and piece2.piece_type == chess.QUEEN:
                        queens += 1
                if queens > 0:
                    if piece.color == chess.WHITE:
                        score += pst_king[sq ^ 56]
                    else:
                        score -= pst_king[sq]
                else:
                    if piece.color == chess.WHITE:
                        score += pst_king_endgame[sq ^ 56]
                    else:
                        score -= pst_king_endgame[sq]                  



    # return table[sq] if color == WHITE else table[sq ^ 56]
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

engine_white = not white

if white:
    move()


while not board.is_game_over():
    subprocess.run("clear")
    print("\"No son, we have Stockfish at home.\"")
    print("You are playing as white.") if white else print("You are playing as black.")

    if True:
        bestmoves = []
        bestscore = None
        # Depth calculation (2-ply)
        for m1 in list(board.legal_moves):
            board.push(m1)

            if board.is_checkmate():
                if engine_white: score = 999999
                else: score = -999999
            elif board.is_game_over():
                score = 0
            else:
                replies = []
                for m2 in list(board.legal_moves):
                    board.push(m2)
                    replies.append(evaluate()) # negative score is better for black
                    board.pop()
                score = min(replies) if engine_white else max(replies)
                print(replies)
            board.pop()
            better = (bestscore is None or (score > bestscore if engine_white else score < bestscore))

            if better:
                bestscore = score
                bestmoves = [m1]
            elif score == bestscore:
                bestmoves.append(m1)

      
        result = random.choice(bestmoves)
        print(bestmoves)
        print(result)
        # print(replies)
        print("\n")
        print(list(board.legal_moves))

    print("Engine plays:", board.san(result))
    board.push(result)

    move()

print("done")
print(board)
print(board.outcome().termination)
print(board.outcome().winner)