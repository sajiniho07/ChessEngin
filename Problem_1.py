import cv2
import numpy as np
import os

def get_file_count():
    folder_path = "res/templates/source"
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            count += 1
    return count

def crop_image_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_value = 100
    _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    croped_img = image[y:y+h, x:x+w]
    return croped_img

def template_maker(image, prefix_name):
    height, width, _ = image.shape
    square_size = height // 8
    for i in range(8):
        for j in range(8):
            x = j * square_size
            y = i * square_size
            square_img = image[y:y+square_size, x:x+square_size]
            
images_count = get_file_count()
for i in range(1, images_count + 1):
    img = cv2.imread(f'res/templates/img ({i}).png')
    new_img = crop_image_border(img)
