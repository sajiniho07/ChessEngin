import cv2
import os
import re
import pandas as pd

import chess
img = cv2.imread("res/Problem03/test/img1.png")

cv2.imshow('Sharpened Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


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
