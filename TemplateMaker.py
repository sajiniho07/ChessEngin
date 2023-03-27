import cv2
import numpy as np

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
            hsv_img = cv2.cvtColor(square_img, cv2.COLOR_BGR2HSV)
            hue, sat, val = cv2.split(hsv_img)
            unique_colors = np.unique(hue)
            num_colors = len(unique_colors)
            if num_colors > 2:
                cv2.imwrite(prefix_name + f'_{i*8+j}.png', square_img)

for i in range(1, 31):
    img = cv2.imread(f'res/templates/img ({i}).png')
    new_img = crop_image_border(img)
    template_maker(new_img, f'{i}')
