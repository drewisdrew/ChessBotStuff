# drewfish.py
# not related to chessbld.py
# my first attempt at a chess bot
import chess
import chess.engine
import subprocess
import random
import os
from colorama import Fore, Style, init
init()

print("Loading engine...")
try:
    if "nt" in os.name:
        nt = True
        engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\andre\\Downloads\\stockfish-windows-arm64-universal\\stockfish\\stockfish-windows-arm64-universal.exe")
    elif "posix" in os.name:
        nt = False
        engine = chess.engine.SimpleEngine.popen_uci("/home/drew/Downloads/stockfish/stockfish-linux-x86-64-universal")
    else:
        print("Unexpected OS.")
except FileNotFoundError:
    print("Make sure the engine in in the directory.")
    print("You can change the directory on lines 14/16 depending on your OS.")
print("Engine loaded.")

game_moves = []
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
0,  0,  0,  5,  5,  5,  0,  0
]

pst_queen = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
-5,  0,  5,  5,  5,  5,  0, -5,
-5,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]

pst_queen_earlygame = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-5,  0,  0,  0,  0,  0,  0, -5,
-5,  0,  0,  0,  0,  0,  0, -5,
-10,  5,  5,  5,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  0,  0,-10,
-20,-10,-10, 15, 15, -10,-10,-20
]

pst_king = [
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
10,  5, -10,-10,-10,-10, 5,  10,
20, 30, 30,  0,  0, 10, 30, 20
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

alt_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
alt_board = "5r1k/ppp3pp/7N/3Q4/8/8/PPP2PPP/6K1 w - - 0 1"
board = chess.Board(alt_board) # if need nerf

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
    totalvalue = 0
    stage = 1
    for piece in board.piece_map().values():
        value = piece_values.get(piece.piece_type)
        if piece.piece_type != chess.PAWN:
            totalvalue += piece_values.get(piece.piece_type)
        score += value if piece.color == chess.WHITE else -value

    if totalvalue < 1500:
        stage = 2
    elif totalvalue > 4500:
        stage = 0

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
                if stage > 0:
                    if piece.color == chess.WHITE:
                        score += pst_queen[sq ^ 56]
                    else:
                        score -= pst_queen[sq]
                else:
                    if piece.color == chess.WHITE:
                        score += pst_queen_earlygame[sq ^ 56]
                    else:
                        score -= pst_queen_earlygame[sq]

            else: # chess.KING
                if stage < 2:
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

def move():
    global game_moves

    while not board.is_game_over():
        move = input("Move (SAN): ")
        try:
            board.parse_san(move)
            game_moves.append(board.parse_uci(board.parse_san(move).uci()))
            board.push_san(move)
            break
        except ValueError:
            if move == "pop":
                board.pop()
                board.pop()
                print(board)
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
    elif board.is_game_over() or board.is_repetition(3):
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

def calculate(depth, review, verbose, full_window):
    best_moves, best_score, moves_all, moves_all_score = [], None, [], []
    mover_white = board.turn == chess.WHITE

    # review means game review feature
    if review:
        checks = [review]
    else:
        checks = list(board.legal_moves)

    for move in checks:
        # print(best_score, best_moves)
        if best_score is None or full_window:
            alpha, beta = -float("inf"), float("inf")
        elif mover_white:
            alpha, beta = best_score - 1, float("inf")
        else:
            alpha, beta = -float("inf"), best_score + 1


        board.push(move)
        score = minmax(alpha, beta, depth - 1, not mover_white)    
        board.pop()
        if verbose: print(score, board.san(move))
        moves_all_score.append(score)
        moves_all.append(move)


        if best_score is None or (score > best_score if mover_white else score < best_score):
            best_score, best_moves = score, [move]
        elif score == best_score:
            best_moves.append(move)
    
    return random.choice(best_moves), best_score, moves_all, moves_all_score


def material(board: chess.Board, color: chess.Color) -> int:
    return sum(
        len(board.pieces(piece_type, color)) * value
        for piece_type, value in piece_values.items()
    )

def material_diff(b, color):
    # material balance from color's perspective
    return material(b, color) - material(b, not color)

def settled_material(b, color):
    # material diff for color once both sides stop capturing
    def q(alpha, beta):
        stand = material_diff(b, b.turn)
        if stand >= beta: return beta
        alpha = max(alpha, stand)
        for m in list(b.legal_moves):
            if b.is_capture(m):
                b.push(m)
                s = -q(-beta, -alpha)
                b.pop()
                if s >= beta: return beta
                alpha = max(alpha, s)
        return alpha
    s = q(-10**6, 10**6)
    return s if b.turn == color else -s

def sacrificed(move):
    mover = board.turn
    before = material_diff(board, mover)
    after = board.copy()
    after.push(move)
    return settled_material(after, mover) <= before - 200

def classify(move):
    white = board.turn == chess.WHITE
    _, _, moves, scores = calculate(5, None, False, full_window=True)
    sign = 1 if white else -1
    cp = {m: max(-3000, min(3000, s * sign)) for m, s in zip(moves, scores)}  

    ranked = sorted(cp.values(), reverse=True)
    loss = ranked[0] - cp[move]

    if loss == 0:
        if sacrificed(move):                   
            return Fore.CYAN + "brilliant" + Style.RESET_ALL
        if len(ranked) > 1 and ranked[0] - ranked[1] >= 150:
            return Fore.BLUE + "great" + Style.RESET_ALL
        return Fore.GREEN + "best" + Style.RESET_ALL
    if loss <= 20:  return Fore.GREEN + "excellent" + Style.RESET_ALL
    if loss <= 50:  return Fore.GREEN + "good" + Style.RESET_ALL
    if loss <= 100: return "an " + Fore.YELLOW + "inaccuracy" + Style.RESET_ALL
    if loss <= 300: return "a " + Fore.YELLOW + "mistake" + Style.RESET_ALL
    return "a " + Fore.RED + "blunder" + Style.RESET_ALL





        
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
    print(board)
    move()


while not board.is_game_over():
    if nt:
        os.system("cls")
    else:
        subprocess.run("clear")
    print("\"No son, we have Stockfish at home.\"")
    print("You are playing as white.") if white else print("You are playing as black.")


    # Depth calculation (n-ply)
    result = calculate(5, None, True, False)
    print("Engine plays:", board.san(result[0]), "(" + str(result[1]) + ")")
    board.push(result[0])
    game_moves.append(result[0])

    print(board)
    move()


print(board.ply() * 2)
print(board.outcome().termination)
print(board.outcome().winner)
print("Enter to see game review.")
input()


board = chess.Board(alt_board)
print(game_moves)
for i, j in enumerate(game_moves):
    print(j)
    print("Move", i)
    result_move = calculate(5, j, False, False)
    result = calculate(5, None, True, False)
    print("DrewFish thinks", board.san(j), "is", classify(j), "and is worth", result_move[1])
    print("DrewFish thinks", board.san(result[0]), "is best and is worth", result_move[1])
    result_bot = engine.play(board, chess.engine.Limit(time=0.1)).move
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = info["score"]
 
    print("Stockfish thinks", board.san(result_bot), "is best and is worth", score.white().score(mate_score=999999)) # STOCKFISH

    board.push(j)
    print(board)
    input("Continue: ")
