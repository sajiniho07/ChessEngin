import cv2
import os
import re


black_tem_path = "res/templates_prob_2/black/"
black_file_list = os.listdir(black_tem_path)


for filename in black_file_list:
    result = re.findall(r"(?<=_)\d+", filename)[0]
    print(result)


# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
