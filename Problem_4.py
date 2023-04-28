import cv2
import os
import pandas as pd
import numpy as np
import chess
from skimage.metrics import structural_similarity as ssim

def count_files_with_extension(path, extension):
    return int(len([f for f in os.listdir(path) if f.endswith(extension)]) / 2)

def medianBlur(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_median = cv2.medianBlur(gray_img, 3)
    return img_median

def sharp_image(img):
    kernel = np.array([[-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
        ])
    sharp = cv2.filter2D(img, -1, kernel)
    return sharp

def crop_image_border(image):
    cropped_img = image[5:123, 5:123]
    resized_img = cv2.resize(cropped_img, (120, 120), interpolation=cv2.INTER_AREA)
    return resized_img

def populate_board(image, mask, board, piece_type, piece_color):
    mask = mask[1:14, 1:14]
    mask_median = medianBlur(mask)
    mask_sharp = sharp_image(mask_median)
    height, width, _ = image.shape
    square_size = height // 8
    for i in range(8):
        for j in range(8):
            x = j * square_size
            y = i * square_size
            square_img = image[y:y+square_size, x:x+square_size]
            square_img = square_img[1:14, 1:14]
            square_median = medianBlur(square_img)
            square_sharp = sharp_image(square_median)
            
            (score, diff) = ssim(square_sharp, mask_sharp, full=True)
            if score > 0.6:
                piece = chess.Piece(piece_type, piece_color)
                board.set_piece_at(chess.square(j, 7 - i), piece)

def get_piece_type(filename):
    name = filename.split(".")[1]
    if name == 'BISHOP':
        return chess.BISHOP
    elif name == 'KING':
        return chess.KING
    elif name == 'KNIGHT':
        return chess.KNIGHT
    elif name == 'QUEEN':
        return chess.QUEEN
    elif name == 'ROOK':
        return chess.ROOK
    else:
        return chess.PAWN

def get_fen_from_board(img):
    black_tem_path = "res/templates_labeled_name/black/"
    black_file_list = os.listdir(black_tem_path)

    white_tem_path = "res/templates_labeled_name/white/"
    white_file_list = os.listdir(white_tem_path)
    new_img = crop_image_border(img)
    
    board = chess.Board(fen='8/8/8/8/8/8/8/8 w - - 0 1')
    for filename in black_file_list:
        piece_type = get_piece_type(filename)
        mask = cv2.imread(os.path.join(black_tem_path, filename))
        populate_board(new_img, mask, board, piece_type, chess.BLACK)

    for filename in white_file_list:
        piece_type = get_piece_type(filename)
        mask = cv2.imread(os.path.join(white_tem_path, filename))
        populate_board(new_img, mask, board, piece_type, chess.WHITE)
        
    return board.fen()

def get_move(board_before, board_after):
    diffs1 = list(board_before.piece_map().items() - board_after.piece_map().items())
    diffs2 = list(board_after.piece_map().items() - board_before.piece_map().items())

    move = "0000"
    is_white_moved = True
    diffs1_len = len(diffs1)
    diffs2_len = len(diffs2)

    if (diffs1_len == 2 and diffs2_len == 2):
        if ((diffs1[0][1].piece_type == chess.ROOK.real and 
            diffs1[1][1].piece_type == chess.KING.real) or 
            (diffs1[0][1].piece_type == chess.KING.real and 
            diffs1[1][1].piece_type == chess.ROOK.real)):
            is_white_moved = (diffs1[0][1].color == chess.WHITE)
            distance = abs(diffs1[0][0] - diffs1[1][0])
            if (distance == 4):
                move = "O-O-O"
            elif (distance == 3):
                move = "O-O"

    elif diffs1_len == 1 and diffs2_len == 1:
        is_white_moved = (diffs2[0][1].color == chess.WHITE)
        if diffs1[0][1] == diffs2[0][1]:
            start_square = chess.square_name(diffs1[0][0])
            end_square = chess.square_name(diffs2[0][0])
            symbol = diffs2[0][1].symbol().upper()
            if diffs2[0][1].piece_type == chess.PAWN.real:
                move = end_square
            elif start_square[0] == end_square[0] or start_square[1] == end_square[1]:
                move = symbol + start_square[0] + end_square
            else:
                move = symbol + end_square

        elif diffs1[0][1].piece_type == chess.PAWN.real and diffs2[0][1].piece_type == chess.QUEEN.real:
            end_square = chess.square_name(diffs2[0][0])
            move = end_square + '=Q'

    elif diffs1_len == 2 and diffs2_len == 1:
        is_white_moved = (diffs2[0][1].color == chess.WHITE)
        if diffs1[0][1] == diffs2[0][1]:
            start_square = chess.square_name(diffs1[0][0])
            end_square = chess.square_name(diffs2[0][0])
            symbol = diffs2[0][1].symbol().upper()
            if diffs2[0][1].piece_type == chess.PAWN.real:
                move = start_square[0] + 'x' + end_square
            else:
                move = symbol + 'x' + end_square

        elif diffs1[1][1] == diffs2[0][1]:
            start_square = chess.square_name(diffs1[1][0])
            end_square = chess.square_name(diffs2[0][0])
            symbol = diffs2[0][1].symbol().upper()
            if diffs2[0][1].piece_type == chess.PAWN.real:
                move = start_square[0] + 'x' + end_square
            else:
                move = symbol + 'x' + end_square

    try:
        fen_before = board_before.fen()
        components = fen_before.split()
        if is_white_moved:
            components[1] = 'w'
        else:
            components[1] = 'b'
        fen = ' '.join(components)
        board_cp = chess.Board(fen)
        board_cp.push_san(move)
    except Exception as e:
        pass

    if board_cp.is_check():
        if board_cp.is_checkmate():
            move += "#"
        else:
            move += "+"

    return move

# folder_path = "res/templates_labeled_name/source"
folder_path = "res/Problem04/test"
predictions = []
images_count = count_files_with_extension(folder_path, ".png")

for i in range(0, images_count):
    img_before = cv2.imread(os.path.join(folder_path, f'img{i}_before.png'))
    fen_before = get_fen_from_board(img_before)
    board_before = chess.Board(fen_before)
    
    img_after = cv2.imread(os.path.join(folder_path, f'img{i}_after.png'))
    fen_after = get_fen_from_board(img_after)
    board_after = chess.Board(fen_after)
    
    move = get_move(board_before, board_after)
    predictions.append((f'img{i}', move))
    print(f'image_log: {i}')

headers = ['image', 'label']
df = pd.DataFrame(predictions, columns=headers)
df.to_csv('predictions.csv', index=False)
