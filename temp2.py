import chess
import cv2


# # o-o-o
# fen_before = "r3k2r/1pqb1pQ1/p1p1p3/2bpN3/3P4/2NBP3/PP3PP1/R4RK1 w - - 0 1"
# fen_after = "2kr3r/1pqb1pQ1/p1p1p3/2bpN3/3P4/2NBP3/PP3PP1/R4RK1 w - - 0 1"

# board_before = chess.Board(fen_before)
# board_after = chess.Board(fen_after)


# diff = board_before.epd() != board_after.epd()

# if diff:
#     new_var1 = set(board_before.piece_map().keys())
#     new_var2 = set(board_after.piece_map().keys())
#     pieces_diff = new_var2 - new_var1
#     new_var = board_before.piece_map()[pieces_diff.pop()]
#     print(f"The different piece is {new_var}")

# ------------------ is chek or mate
fen = "1k5r/bpp5/p7/2P1NQ2/1P3p1r/P2P4/5PK1/4RR2 w - - 0 1"

board = chess.Board(fen)
board_cp = board.copy()
try:
    board_cp.push_san("Rhh2")
except Exception as e:
    pass
if board_cp.is_check() and board_cp.turn == chess.WHITE:
    if board_cp.is_checkmate():
        print("White king is checkmated!")
    else:
        print("White king is in check")
else:
    print("White king is not in check")

if board_cp.is_check() and board_cp.turn == chess.BLACK:
    if board_cp.is_checkmate():
        print("Black king is checkmated!")
    else:
        print("Black king is in check")
else:
    print("Black king is not in check")

# ---------------------


# img = cv2.imread("res/Problem04/train/img1401_before.png")
# cv2.imshow("image", img)
# img = cv2.imread("res/Problem04/train/img1401_after.png")
# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# board = chess.Board()

# # Make a sample move
# move = chess.Move.from_uci("g1f3")
# print(move.uci)

