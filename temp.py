import cv2
import os
import re
import pandas as pd
import chess

# Ne3
# fen_before = "r6r/pp5p/2p4k/2bNpPp1/3nP1P1/6K1/PP1B4/R4B2 w - - 0 1"
# fen_after = "r6r/pp5p/2p4k/2b1pPp1/3nP1P1/4N1K1/PP1B4/R4B2 w - - 0 1"

# cxb4
# fen_before = "5rk1/5p1p/2n3p1/8/1pN3P1/2P1P2q/3PQ3/1R2K3 w - - 0 1"
# fen_after = "5rk1/5p1p/2n3p1/8/1PN3P1/4P2q/3PQ3/1R2K3 w - - 0 1"

# o-o-o
fen_before = "r3k2r/1pqb1pQ1/p1p1p3/2bpN3/3P4/2NBP3/PP3PP1/R4RK1 w - - 0 1"
fen_after = "2kr3r/1pqb1pQ1/p1p1p3/2bpN3/3P4/2NBP3/PP3PP1/R4RK1 w - - 0 1"

board_before = chess.Board(fen_before)
board_after = chess.Board(fen_after)

diffs1 = list(board_before.piece_map().items() - board_after.piece_map().items())
diffs2 = list(board_after.piece_map().items() - board_before.piece_map().items())

move = "0000"
diffs1_len = diffs1.__len__()
diffs2_len = diffs2.__len__()
if (diffs1_len == 2 and diffs2_len == 2):
    if (diffs1[0][1].piece_type == chess.ROOK.real and diffs1[1][1].piece_type == chess.KING.real):
        distance = abs(diffs1[0][0] - diffs1[1][0])
        if (distance == 4):
            move = "O-O-O"
        elif (distance == 3):
            mopve = "O-O"
elif (diffs1_len == 1 and diffs2_len == 1):
    if (diffs1[0][1] == diffs2[0][1]):
        start_square = chess.square_name(diffs1[0][0])
        end_square = chess.square_name(diffs2[0][0])
        symbol = diffs2[0][1].symbol()
        if (diffs2[0][1].piece_type == chess.PAWN.real):
            move = end_square
        elif (start_square[0] == end_square[0]):
            move = symbol + start_square[0] + end_square
        else:
            move = symbol + end_square
elif (diffs1_len == 2 and diffs2_len == 1):
    if (diffs1[1][1] == diffs2[0][1]):
        start_square = chess.square_name(diffs1[1][0])
        end_square = chess.square_name(diffs2[0][0])
        symbol = diffs2[0][1].symbol()
        if (diffs2[0][1].piece_type == chess.PAWN.real):
            move = start_square[0] + 'x' + end_square
        else:
            move = symbol + 'x' + end_square
    
print(move)
        # start_square = chess.square_name(diffs1[0][1])
# new_var = chess.Move.from_uci(start_square + end_square)
# if board_after.is_castling(new_var):
#     print(start_square + end_square)

#     # Find the piece that was captured
#     captured_piece = board_before.piece_at(chess.parse_square(end_square))
#     if captured_piece:
#         # Determine the move in standard chess notation with the captured piece
#         move = start_square + 'x' + end_square + str(captured_piece.symbol()).lower()
#     else:
#         # Determine the move in standard chess notation without the captured piece
#         move = start_square + 'x' + end_square
# else:
#     # Determine the move in standard chess notation without capture
#     move = start_square + end_square


# print("The move played was:", move)





# Determine the starting and ending squares
# start_square = chess.square_name(diffs[0][0])
# end_square = chess.square_name(diffs[1][0])

# Determine the move in standard chess notation
# move = start_square + end_square

# print("The move played was:", moved_piece)



# diff = board_before.epd() != board_after.epd()
# if diff:
#     new_var1 = set(board_before.piece_map().keys())
#     new_var2 = set(board_after.piece_map().keys())
#     pieces_diff = new_var1 - new_var2
#     new_var = board_before.piece_map()[pieces_diff.pop()]
#     print(f"The different piece is {new_var}")
    
# move = chess.Move.from_uci('c3b4')
# print(board_before.san(move))





# from_square = board_before.king(board_before.turn)
# to_square = board_after.king(board_after.turn)
# move = chess.Move(from_square, to_square)
# print("move is:", move.uci())




# diff = board_before.epd() != board_after.epd()
# if diff:
#     new_var1 = set(board_before.piece_map().keys())
#     new_var2 = set(board_after.piece_map().keys())
#     pieces_diff = new_var1 - new_var2
#     new_var = board_before.piece_map()[pieces_diff.pop()]
#     print(f"The different piece is {new_var}")

# king_square = board_before.king(board_before.turn)#.square
# piece_type = new_var.piece_type
# color = new_var.color




# new_var3 = chess.SQUARES[board_before.pieces_mask(piece_type, color) ^ 
#                                         board_after.pieces_mask(piece_type, color)].pop()
                  
# to_square = king_square + new_var3
# move = chess.Move(king_square, to_square)

# from_square = board_before.king(board_before.turn)
# to_square = board_after.king(not board_before.turn)
# move = chess.Move(from_square, to_square)
# print("move is:", move.uci())




# king_piece = board_after.piece_at(board_before.king(board_before.turn))
# # to_square = king_piece.square

# king_square = board_before.king(board_before.turn)
# for square, piece in chess.scan_reversed(board_after._board_fen().split()[0], king_square):
#     if piece == chess.Piece(chess.KING, board_before.turn):
#         to_square = square
#         break


# to_square = board_after.piece_at(board_after.king(board_before.turn)).square

# from_square = board_before.king(board_before.turn).square
# to_square = board_after.king(not board_before.turn).square
# move = chess.Move(from_square, to_square)
# print("move is:", move.uci())



# move = board_after.uci(board_after.parse_san(board_before.san(chess.Move.null())))
# print(move)

# diff = board_before.epd() != board_after.epd()

# if diff:
#     new_var1 = set(board_before.piece_map().keys())
#     print(new_var1)
#     new_var2 = set(board_after.piece_map().keys())
#     print(new_var2)
#     pieces_diff = new_var1 - new_var2
#     new_var = board_before.piece_map()[pieces_diff.pop()]
#     print(f"The different piece is {new_var}")


# print(board_temp.legal_moves.__sizeof__())
# print(board_after.legal_moves.__sizeof__())
# print(board_before.legal_moves.__sizeof__())

# for move in board_after.legal_moves:
#     board_temp.legal_moves(move)
#     if board_temp.fen() == board_after.fen():
#         print("fen are same")
#         break


# img = cv2.imread("res/Problem04/train/img4561.png")

# cv2.imshow('Sharpened Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# black_tem_path = "res/templates_labeled_name/rec/white/"
# black_file_list = os.listdir(black_tem_path)

# for filename in black_file_list:
#     img = cv2.imread(os.path.join(black_tem_path, filename))
#     resized_img = cv2.resize(img, (14, 14), interpolation=cv2.INTER_AREA)
#     cv2.imwrite(filename, resized_img)

# img = cv2.imread("res/Problem03/test/img4561.png")

# cv2.imshow('Sharpened Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# board = chess.Board()
# board.set_fen("1b1r1r1k-1p2R1pp-p2PQnp1-2p1N1B1-8-7P-PqP2PP1-4R1K1 b KQkq - 0 3")

# print(board.fen())

# black_tem_path = "res/templates_prob_2/black/"
# black_file_list = os.listdir(black_tem_path)


# for filename in black_file_list:
#     result = re.findall(r"(?<=_)\d+", filename)[0]
#     print(result)


# img = cv2.imread("res/Problem03/test/img0.png")
# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
