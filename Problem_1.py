import cv2
import os
import pandas as pd

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

folder_path = "res/Problem01/test"
predictions = []
images_count = count_files_with_extension(folder_path, ".png")

for i in range(0, images_count):
    img = cv2.imread(os.path.join(folder_path, f'img{i}.png'))
    new_img = crop_image_border(img)

    black_cnt = sum(get_similar_mask_cnt(new_img, cv2.imread(os.path.join("res/templates/black", f'{j}.png'))) for j in range(1, 13))
    white_cnt = sum(get_similar_mask_cnt(new_img, cv2.imread(os.path.join("res/templates/white", f'{j}.png'))) for j in range(1, 13))

    label = -1
    if white_cnt > black_cnt:
        label = 1
    elif black_cnt > white_cnt:
        label = 0
        
    predictions.append((f'img{i}', label))
    print(f'image: {i}')

headers = ['image', 'label']
df = pd.DataFrame(predictions, columns=headers)
df.to_csv('predictions.csv', index=False)
