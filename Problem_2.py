import cv2
import os
import pandas as pd
import re

def count_files_with_extension(path, extension):
    return len([f for f in os.listdir(path) if f.endswith(extension)])

def crop_image_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_value = 100
    _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_img = image[y:y+h, x:x+w]
    return cropped_img

def get_similar_mask_cnt(image, mask):
    height, width, _ = image.shape
    square_size = height // 8
    similar_cnt = sum(1 for i in range(8) for j in range(8)
                       if cv2.minMaxLoc(cv2.matchTemplate(
                           image[i*square_size:(i+1)*square_size, j*square_size:(j+1)*square_size],
                           mask, 
                           cv2.TM_CCOEFF_NORMED))[1] >= 0.8)
    return similar_cnt

black_tem_path = "res/templates_labeled_score/black/"
black_file_list = os.listdir(black_tem_path)

white_tem_path = "res/templates_labeled_score/white/"
white_file_list = os.listdir(white_tem_path)

folder_path = "res/Problem02/test"
predictions = []
images_count = count_files_with_extension(folder_path, ".png")

for i in range(0, images_count):
    img = cv2.imread(os.path.join(folder_path, f'img{i}.png'))
    new_img = crop_image_border(img)

    black_total_score = sum(get_similar_mask_cnt(new_img, cv2.imread(os.path.join(black_tem_path, filename))) * 
                            int(re.findall(r"(?<=_)\d+", filename)[0]) 
                            for filename in black_file_list)

    white_total_score = sum(get_similar_mask_cnt(new_img, cv2.imread(os.path.join(white_tem_path, filename))) * 
                            int(re.findall(r"(?<=_)\d+", filename)[0]) 
                            for filename in white_file_list)
    label = -1
    if white_total_score > black_total_score:
        label = 1
    elif black_total_score > white_total_score:
        label = 0
        
    predictions.append((f'img{i}', label))
    print(f'image: {i}', f' -- {label} -- tws: {white_total_score}', f' ---- tbs: {black_total_score}')

headers = ['image', 'label']
df = pd.DataFrame(predictions, columns=headers)
df.to_csv('predictions.csv', index=False)
