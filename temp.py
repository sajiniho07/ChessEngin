import os

folder_path = "res/Problem01/test"
count = 0

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        count += 1

print("تعداد فایل‌های png در پوشه: ", count)
