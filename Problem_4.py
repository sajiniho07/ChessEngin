import cv2
import os
import pandas as pd
import chess
from skimage.metrics import structural_similarity as ssim

def count_files_with_extension(path, extension):
    return int(len([f for f in os.listdir(path) if f.endswith(extension)]) / 2)

def crop_image_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_value = 130
    _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_img = image[x:x+w, x:x+w]
    resized_img = cv2.resize(cropped_img, (120, 120), interpolation=cv2.INTER_AREA)
    return resized_img

def populate_board(image, mask, board, piece_type, piece_color):
    height, width, _ = image.shape
    square_size = height // 8
    for i in range(8):
        for j in range(8):
            x = j * square_size
            y = i * square_size
            square_img = image[y:y+square_size, x:x+square_size]
            gray_img1 = cv2.cvtColor(square_img, cv2.COLOR_BGR2GRAY)
            gray_img2 = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            
            (score, diff) = ssim(gray_img1, gray_img2, full=True)
            if score > 0.7:
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
    diffs1_len = diffs1.__len__()
    diffs2_len = diffs2.__len__()
    if (diffs1_len == 2 and diffs2_len == 2):
        if (diffs1[0][1].piece_type == chess.ROOK.real and diffs1[1][1].piece_type == chess.KING.real):
            distance = abs(diffs1[0][0] - diffs1[1][0])
            if (distance == 4):
                move = "O-O-O"
            elif (distance == 3):
                move = "O-O"
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
    return move

folder_path = "res/templates_labeled_name/source"
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
    predictions.append((f'img{i}', move, board_before.fen(), board_after.fen()))
    print(f'image_log: {i}')

headers = ['image', 'label', 'board_before', 'board_after']
df = pd.DataFrame(predictions, columns=headers)
df.to_csv('predictions.csv', index=False)
