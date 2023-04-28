import cv2
import numpy as np
import os

def crop_image_border(image):
    cropped_img = image[5:123, 5:123]
    resized_img = cv2.resize(cropped_img, (120, 120), interpolation=cv2.INTER_AREA)
    return resized_img

def template_maker(image, prefix_name):
    height, width, _ = image.shape
    square_size = height // 8
    for i in range(8):
        for j in range(8):
            x = j * square_size
            y = i * square_size
            square_img = image[y:y+square_size, x:x+square_size]
            hsv_img = cv2.cvtColor(square_img, cv2.COLOR_BGR2HSV)
            hue, sat, val = cv2.split(hsv_img)
            unique_colors = np.unique(hue)
            num_colors = len(unique_colors)
            if num_colors > 2:
                cv2.imwrite(prefix_name + f'_{i*8+j}.png', square_img)

main_source_path = "res/Problem04/test/"
main_file_list = os.listdir(main_source_path)

for i in range(5, 6):
    img_before = cv2.imread(os.path.join(main_source_path, f'img{i}_after.png'))
    new_img = crop_image_border(img_before)
    template_maker(new_img, f'{i}')
