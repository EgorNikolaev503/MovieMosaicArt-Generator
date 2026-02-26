# Код для создания и сохранения словаря
# Индексирует картинки по цвету {(r, g, b): ["путь к изображению"]}
import os
from PIL import Image
from collections import defaultdict
import json

def get_average_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        pixels = list(img.getdata())
        r = sum(pixel[0] for pixel in pixels) // len(pixels)
        g = sum(pixel[1] for pixel in pixels) // len(pixels)
        b = sum(pixel[2] for pixel in pixels) // len(pixels)
    return (r, g, b)

color_to_paths = defaultdict(list)
folder_path = 'images' # название папки в которую был распакован архив нужно вписать тут

j = 0
for filename in os.listdir(folder_path):
    j += 1
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, filename)
        avg_color = get_average_color(image_path)
        color_to_paths[avg_color].append(image_path)
        print(j)

with open('color_dict.json', 'w') as f:
    json.dump({str(k): v for k, v in color_to_paths.items()}, f)