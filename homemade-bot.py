# homemade-bot.py
# not related to chessbld.py
# my first attempt at a chess bot
import chess
import subprocess
import random
import os

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
-20,-10,-10, 10, -5,-10,-10,-20,
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
10,  5, -10,-10,-10,-10, 5,  10,
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

    endgame = True
    for sq2 in chess.SQUARES:
        piece2 = board.piece_at(sq2)
        if piece2 and piece2.piece_type == chess.QUEEN:
            endgame = False
            break

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    score += pst_pawn[sq ^ 56]
                else:
                    score -= pst_pawn[sq]

            elif piece.piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    score += pst_knight[sq ^ 56]
                else:
                    score -= pst_knight[sq]

            elif piece.piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    score += pst_bishop[sq ^ 56]
                else:
                    score -= pst_bishop[sq]

            elif piece.piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    score += pst_rook[sq ^ 56]
                else:
                    score -= pst_rook[sq]

            elif piece.piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    score += pst_queen[sq ^ 56]
                else:
                    score -= pst_queen[sq]

            else: # chess.KING
                if not endgame:
                    if piece.color == chess.WHITE:
                        score += pst_king[sq ^ 56]
                    else:
                        score -= pst_king[sq]
                else:
                    if piece.color == chess.WHITE:
                        score += pst_king_endgame[sq ^ 56]
                    else:
                        score -= pst_king_endgame[sq]

    # Penalize being in check
    if board.is_check():
        if board.turn == chess.WHITE:
            score -= 25
        else:
            score += 25                  


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


def move_order_key(move):
    # search captures and promotions first
    score = 0
    if board.is_capture(move):
        victim = board.piece_at(move.to_square)
        victim_value = piece_values[victim.piece_type] if victim else 100 # account for en passant
        attacker = board.piece_at(move.from_square)
        attacker_value = piece_values[attacker.piece_type]
        score += 10 * victim_value - attacker_value
    if move.promotion:
        score += piece_values[move.promotion]
    return -score



def minmax(alpha, beta, depth, maxxing):
    if board.is_checkmate():
        return -(999999 + depth) if maxxing else (999999 + depth)
    elif board.is_game_over():
        return 0
    if depth == 0:
        return evaluate()

    moves = sorted(board.legal_moves, key=move_order_key)
    if maxxing:
        best = -float("inf")
        for move in moves:
            board.push(move)
            best = max(best, minmax(alpha, beta, depth - 1, False))
            board.pop()
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float("inf")
        for move in moves:
            board.push(move)
            best = min(best, minmax(alpha, beta, depth - 1, True))
            board.pop()
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best

def calculate(depth):
    best_moves, best_score = [], None
    for move in list(board.legal_moves):

        if best_score is None:
            alpha, beta = -float("inf"), float("inf")
        elif engine_white:
            alpha, beta = best_score - 1, float("inf")
        else:
            alpha, beta = -float("inf"), best_score + 1


        board.push(move)
        score = minmax(alpha, beta, depth - 1, not engine_white)
        board.pop()

        if best_score is None or (score > best_score if engine_white else score < best_score):
            best_score, best_moves = score, [move]
        elif score == best_score:
            best_moves.append(move)
    print(best_score)
    return random.choice(best_moves)


        
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
    if "nt" in os.name:
        os.system("cls")
    else:
        subprocess.run("clear")
    print("\"No son, we have Stockfish at home.\"")
    print("You are playing as white.") if white else print("You are playing as black.")


    # Depth calculation (n-ply)
    result = calculate(5)
    print("Engine plays:", board.san(result))
    board.push(result)

    move()

print("done")
print(board)
print(board.outcome().termination)
print(board.outcome().winner)