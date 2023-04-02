import cv2
import os
import pandas as pd
import chess
from skimage.metrics import structural_similarity as ssim

def count_files_with_extension(path, extension):
    return len([f for f in os.listdir(path) if f.endswith(extension)])

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

black_tem_path = "res/templates_labeled_name/black/"
black_file_list = os.listdir(black_tem_path)

white_tem_path = "res/templates_labeled_name/white/"
white_file_list = os.listdir(white_tem_path)

#main_source_path = "res/templates_labeled_name/source/"
folder_path = "res/Problem03/test"
predictions = []
images_count = count_files_with_extension(folder_path, ".png")

for i in range(0, images_count):
    img = cv2.imread(os.path.join(folder_path, f'img{i}.png'))
    new_img = crop_image_border(img)
    board = chess.Board(fen='8/8/8/8/8/8/8/8 w - - 0 1')
    for filename in black_file_list:
        name = filename.split(".")[1]
        piece_type = chess.PAWN
        if name == 'BISHOP':
            piece_type = chess.BISHOP
        elif name == 'KING':
            piece_type = chess.KING
        elif name == 'KNIGHT':
            piece_type = chess.KNIGHT
        elif name == 'QUEEN':
            piece_type = chess.QUEEN
        elif name == 'ROOK':
            piece_type = chess.ROOK
        mask = cv2.imread(os.path.join(black_tem_path, filename))
        populate_board(new_img, mask, board, piece_type, chess.BLACK)

    for filename in white_file_list:
        name = filename.split(".")[1]
        piece_type = chess.PAWN
        if name == 'BISHOP':
            piece_type = chess.BISHOP
        elif name == 'KING':
            piece_type = chess.KING
        elif name == 'KNIGHT':
            piece_type = chess.KNIGHT
        elif name == 'QUEEN':
            piece_type = chess.QUEEN
        elif name == 'ROOK':
            piece_type = chess.ROOK
        mask = cv2.imread(os.path.join(white_tem_path, filename))
        populate_board(new_img, mask, board, piece_type, chess.WHITE)
        
    fen_str = board.fen().split(" ")[0]
    predictions.append((f'img{i}', fen_str))
    print(f'image_log: {i}')

headers = ['image', 'label']
df = pd.DataFrame(predictions, columns=headers)
df.to_csv('predictions.csv', index=False)
